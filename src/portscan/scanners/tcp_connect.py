import asyncio 
from contextlib import suppress
from dataclasses import dataclass
from typing import Optional
from portscan.logging_config import get_logger
from portscan.services.probes import (probe_http, probe_https, probe_ssh, probe_smtp, probe_ftp)

logger = get_logger(__name__)

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

    def __init__(self, timeout: float = 0.8, banner_timeout: float = 0.5, banner_bytes: int = 128, retries: int = 0, retry_delay: float = 0.2):
        self.timeout = timeout
        self.banner_timeout = banner_timeout  # Increased default from 0.1 to 0.5
        self.banner_bytes = banner_bytes
        self.retries = max(0, int(retries))
        self.retry_delay = max(0.0, float(retry_delay))
        
        logger.debug(f"TCPConnectScanner initialized: timeout={timeout}s, banner_timeout={banner_timeout}s, retries={retries}")

    async def probe(self, host: str, port: int) -> ProbeResult:
        attempts = self.retries + 1
        last_exc: Optional[BaseException] = None

        for i in range(attempts):
            try:
                logger.debug(f"Probing {host}:{port} (attempt {i+1}/{attempts})")
                
                #Open Connection
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(host, port), 
                    timeout=self.timeout
                )
                
                logger.debug(f"Connected to {host}:{port}")

                #Attempt to grab banner
                banner = None
                try:
                    data = await asyncio.wait_for(
                        reader.read(self.banner_bytes), 
                        timeout=self.banner_timeout
                    )
                    
                    if data: 
                        banner = data.decode(errors="ignore").strip()
                        logger.debug(f"Banner from {host}:{port}: {banner[:60]}{'...' if len(banner) > 60 else ''}")
                    else:
                        logger.debug(f"No banner data from {host}:{port}")
                        
                except asyncio.TimeoutError:
                    logger.debug(f"Banner grab timeout on {host}:{port}")
                except Exception as e:
                    logger.debug(f"Banner grab failed on {host}:{port}: {type(e).__name__}")

                
                #Service Identification Probes
                service = None
                extra_banner = None
                try:
                    probe_timeout = self.timeout

                    if port in (80, 8080, 8000, 8081):
                        logger.debug(f"Attempting HTTP probe on {host}:{port}")
                        service, extra_banner = await probe_http(host, port, timeout=probe_timeout)
                    elif port in (443, 8443, 9443):
                        logger.debug(f"Attempting HTTPS probe on {host}:{port}")
                        service, extra_banner = await probe_https(host, port, timeout=probe_timeout)
                    elif port == 22:
                        logger.debug(f"Attempting SSH probe on {host}:{port}")
                        service, extra_banner = await probe_ssh(host, port, timeout=probe_timeout)
                    elif port == 25:
                        logger.debug(f"Attempting SMTP probe on {host}:{port}")
                        service, extra_banner = await probe_smtp(host, port, timeout=probe_timeout)
                    elif port == 21:
                        logger.debug(f"Attempting FTP probe on {host}:{port}")
                        service, extra_banner = await probe_ftp(host, port, timeout=probe_timeout)
                    
                    if service:
                        logger.debug(f"Service detected on {host}:{port}: {service}")
                        
                except asyncio.TimeoutError:
                    logger.debug(f"Service probe timeout on {host}:{port}")
                except Exception as e:
                    logger.debug(f"Service probe failed on {host}:{port}: {type(e).__name__}: {e}")

                final_banner = extra_banner or banner

                #Close and Clean up Connection
                writer.close()
                with suppress(Exception):
                    await writer.wait_closed()

                logger.debug(f"Port {host}:{port} is OPEN")
                return ProbeResult(host, port, "tcp", "open", banner=final_banner, reason="connect-ok", service=service)
            
            except asyncio.TimeoutError as e:
                logger.debug(f"Timeout connecting to {host}:{port}")
                last_exc = e
                if i < attempts - 1:
                    logger.debug(f"Retrying {host}:{port} after {self.retry_delay}s delay")
                    if self.retry_delay:
                        await asyncio.sleep(self.retry_delay)
                    continue
                break
                
            except ConnectionRefusedError as e:
                logger.debug(f"Connection refused: {host}:{port}")
                last_exc = e
                break  #No point retrying refused connections
                
            except OSError as e:
                logger.debug(f"OS error connecting to {host}:{port}: {e}")
                last_exc = e
                break  #Network errors typically won't resolve with retries
                
            except Exception as e:
                logger.debug(f"Unexpected error probing {host}:{port}: {type(e).__name__}: {e}")
                last_exc = e
                break

        #Log closed/filtered ports at debug level
        reason = type(last_exc).__name__ if last_exc else "unknown"
        logger.debug(f"Port {host}:{port} is CLOSED (reason: {reason})")
        return ProbeResult(host, port, "tcp", "closed", reason=reason)