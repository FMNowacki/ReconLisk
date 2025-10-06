import socket
import asyncio
import binascii
import struct
import datetime
from dataclasses import dataclass
from typing import Optional, Dict

from .tcp_connect import ProbeResult

#Small payloads for some known services
UDP_PROBES: Dict[int, bytes] = {
    53: b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01",
    123: b"\x1b" + 47 * b"\0",  # NTP
    161: b"\x30\x26\x02\x01\x01\x04\x06public\xa0\x19\x02\x04\x71\x39\x06\x56\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00",
}


#Helpers for banner display 
def sanitize_text(data: bytes, max_len: int = 120) -> str:
    """Printable characters left, others -> '.'; truncated to max_len."""
    out = []
    for b in data[:max_len]:
        if 32 <= b <= 126:  #printable ASCII
            out.append(chr(b))
        else:
            out.append(".")
    s = "".join(out)
    if len(data) > max_len:
        s += "..."
    return s

def hex_dump(data: bytes, max_bytes: int = 64) -> str:
    """Compact hex representation truncated to max_bytes."""
    if not data:
        return ""
    d = data[:max_bytes]
    h = binascii.hexlify(d).decode()
    if len(data) > max_bytes:
        return h + "..."
    return h

def try_decode_text(data: bytes, max_len: int = 120) -> str:
    """Try UTF-8 decode, otherwise fallbacks to sanitized text."""
    try:
        s = data.decode("utf-8", errors="strict")
        s = s.replace("\r", "\\r").replace("\n", "\\n")
        return s[:max_len] + ("..." if len(s) > max_len else "")
    except Exception:
        return sanitize_text(data, max_len=max_len)


#Protocol parsers
def parse_ntp(data: bytes) -> Optional[dict]:
    """Parse basic NTP header fields; return dict or None on failure."""
    if len(data) < 48:
        return None
    try:
        first = data[0]
        li = (first >> 6) & 0x3
        vn = (first >> 3) & 0x7
        mode = first & 0x7
        stratum = data[1]
        #timestamps are 64-bit (sec, frac)
        def ntp_ts_to_datetime(ts_bytes: bytes) -> datetime.datetime:
            sec, frac = struct.unpack("!II", ts_bytes)
            unix_sec = sec - 2208988800  # NTP -> UNIX epoch
            frac_sec = float(frac) / (1 << 32)
            return datetime.datetime.utcfromtimestamp(unix_sec + frac_sec)

        tx_time = ntp_ts_to_datetime(data[40:48])

        return {
            "li": li,
            "vn": vn,
            "mode": mode,
            "stratum": stratum,
            "tx_time": tx_time.isoformat() + "Z",
        }
    except Exception:
        return None

def parse_dns(data: bytes) -> Optional[str]:
    """
    Helper to parse DNS response: returns the first answer type/name truncated,
    or None if parsing fails. (not a full DNS parser).
    """
    if len(data) < 12:
        return None
    try:
        #basic header: ID (2), flags (2), QDCOUNT (2), ANCOUNT (2), NSCOUNT (2), ARCOUNT (2)
        ancount = struct.unpack("!H", data[6:8])[0]
        if ancount == 0:
            return "no-answers"
        return f"DNS response (answers={ancount})"
    except Exception:
        return None


#The actual UDP scanner implementation
@dataclass
class UDPScanner:
    """
    UDP scanner using blocking sockets run in a thread via asyncio.to_thread.
    """
    timeout: float = 1.5
    read_bytes: int = 4096
    retries: int = 1
    retry_delay: float = 0.3

    async def probe(self, host: str, port: int) -> ProbeResult:
        attempts = max(1, int(self.retries) + 1)
        last_reason: Optional[str] = None
        for i in range(attempts):
            res = await asyncio.to_thread(self._probe_sync, host, port)
            if res.state == "open":
                return res
            last_reason = res.reason
            #retries only on ambiguous silence
            if last_reason == "open|filtered" and i < attempts - 1 and self.retry_delay > 0:
                await asyncio.sleep(self.retry_delay)
                continue
            break

        #returns the last observed result (closed) with a reason
        return ProbeResult(host, port, "udp", "closed", reason=last_reason or "unknown")

    def _probe_sync(self, host: str, port: int) -> ProbeResult:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)
        try:
            payload = UDP_PROBES.get(port, b"\x00")
            try:
                sock.sendto(payload, (host, port))
            except OSError as e:
                #local error (e.g. network unreachable)
                return ProbeResult(host, port, "udp", "closed", reason=type(e).__name__)

            try:
                data, _ = sock.recvfrom(self.read_bytes)
                #Builds a banner string
                banner_text: Optional[str] = None

                #Protocol-aware attempts
                if port == 123:
                    info = parse_ntp(data)
                    if info:
                        banner_text = f"NTP v{info['vn']} mode={info['mode']} stratum={info['stratum']} tx={info['tx_time']}"
                elif port == 53:
                    dns_info = parse_dns(data)
                    if dns_info:
                        banner_text = dns_info

                #Fallback: tries to decode text; else sanitized + hex
                if not banner_text:
                    printable = try_decode_text(data, max_len=80)
                    hexpart = hex_dump(data, max_bytes=64)
                    banner_text = f"{printable} (hex={hexpart})" if hexpart else printable

                return ProbeResult(host, port, "udp", "open", banner=banner_text, reason="udp-response")

            except socket.timeout:
                #No response: ambiguous (open or filtered)
                return ProbeResult(host, port, "udp", "closed", reason="open|filtered")
            except ConnectionRefusedError:
                #ICMP port unreachable reported locally => closed
                return ProbeResult(host, port, "udp", "closed", reason="icmp-port-unreachable")
            except OSError as e:
                return ProbeResult(host, port, "udp", "closed", reason=type(e).__name__)
        finally:
            sock.close()
