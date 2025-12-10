import asyncio 
from contextlib import suppress
from dataclasses import dataclass
from typing import Optional
from portscan.services.probes import (probe_http, probe_https, probe_ssh, probe_smtp, probe_ftp)

#Data Container with all the info about a single port probe
@dataclass
class ProbeResult: 
    host: str
    port: int
    proto: str
    state: str
    banner: Optional[str] = None 
    reason: Optional[str] = None
    service: Optional[str] = None

#Scanner Object 
class TCPConnectScanner: 

    def __init__(self, timeout: float = 0.8, banner_timeout = 0.1, banner_bytes: int = 128, retries: int = 0, retry_delay: float = 0.2):
        self.timeout = timeout
        self.banner_timeout = banner_timeout
        self.banner_bytes = banner_bytes
        self.retries = max(0, int(retries))
        self.retry_delay = max(0.0, float(retry_delay))

    async def probe(self, host: str, port: int) -> ProbeResult:
        attempts = self.retries + 1
        last_exc: Optional[BaseException] = None

        for i in range(attempts):
            try: 
                #Open Connection
                reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout = self.timeout)

                #Attempt to grab banner
                banner = None

                with suppress(asyncio.TimeoutError):
                    data = await asyncio.wait_for(reader.read(self.banner_bytes), timeout=self.banner_timeout)

                    if data: 
                        banner = data.decode(errors="ignore").strip()

                
                #Service Identification Probes
                service = None
                extra_banner = None
                try:
                    probe_timeout = self.timeout

                    if port in (80, 8080, 8000, 8081):
                        service, extra_banner = await probe_http(host, port, timeout=probe_timeout)
                    elif port in (443, 8443, 9443):
                        service, extra_banner = await probe_https(host, port, timeout=probe_timeout)
                    elif port == 22:
                        service, extra_banner = await probe_ssh(host, port, timeout=probe_timeout)
                    elif port == 25:
                        service, extra_banner = await probe_smtp(host, port, timeout=probe_timeout)
                    elif port == 21:
                        service, extra_banner = await probe_ftp(host, port, timeout=probe_timeout)
                except Exception:
                    #best effort only
                    pass

                final_banner = extra_banner or banner

                #Close and Clean up Connection
                writer.close()
                with suppress(Exception):
                    await writer.wait_closed()

                return ProbeResult(host, port, "tcp", "open", banner=final_banner, reason="connect-ok", service=service)
            
            except Exception as e:
                last_exc = e
                if isinstance(e, asyncio.TimeoutError) and i < attempts - 1: 
                    if self.retry_delay:
                        await asyncio.sleep(self.retry_delay)
                    continue
                break

        return ProbeResult(host, port, "tcp", "closed", reason=type(last_exc).__name__ if last_exc else "unknown")

