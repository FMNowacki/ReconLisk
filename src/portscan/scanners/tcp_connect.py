import asyncio 
from contextlib import suppress
from dataclasses import dataclass
from typing import Optional

#Data Container with all the info about a single port probe
@dataclass
class ProbeResult: 
    host: str
    port: int
    proto: str
    state: str
    banner: Optional[str] = None 
    reason: Optional[str] = None

#Scanner Object 
class TCPConnectScanner: 

    def __init__(self, timeout: float = 0.8, banner_timeout = 0.1, banner_bytes: int = 128):
        self.timeout = timeout
        self.banner_timout = banner_timeout
        self.banner_bytes = banner_bytes

    async def probe(self, host: str, port: int) -> ProbeResult:
        try: 
            #Open Connection
            reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout = self.timeout)

            #Attempt to grab banner
            banner = None

            with suppress(asyncio.TimeoutError):
                data = await asyncio.wait_for(reader.read(self.banner_bytes), timeout=self.banner_timout)

                if data: 
                    banner = data.decode(errors="ignore").strip()

            #Close and Clean up Connection
            writer.close()
            with suppress(Exception):
                await writer.wait_closed()

            return ProbeResult(host, port, "tcp", "open", banner=banner, reason="connect-ok")
        
        except Exception as e:
            return ProbeResult(host, port, "tcp", "closed", reason=type(e).__name__)

