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

    def __init__(self, timeout: float = 0.8, banner_timeout = 0.1, banner_bytes: int = 128, retries: int = 0, retry_delay: float = 0.2):
        self.timeout = timeout
        self.banner_timeout = banner_timeout
        self.banner_bytes = banner_bytes
        self.retries = max(0, int(retries))
        self.retry_delay = max(0.0, float(retry_delay))

    async def probe(self, host: str, port: int) -> ProbeResult:
        attempts = self.retries + 1
        last_exec: Optional[BaseException] = None

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

                #Close and Clean up Connection
                writer.close()
                with suppress(Exception):
                    await writer.wait_closed()

                return ProbeResult(host, port, "tcp", "open", banner=banner, reason="connect-ok")
            
            except Exception as e:
                last_exc = e
                if isinstance(e, asyncio.TimeoutError) and i < attempts - 1: 
                    if self.retry_delay:
                        await asyncio.sleep(self.retry_delay)
                    continue
                break

        return ProbeResult(host, port, "tcp", "closed", reason=type(last_exc).__name__ if last_exc else "unknown")

