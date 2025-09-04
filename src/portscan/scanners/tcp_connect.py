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

