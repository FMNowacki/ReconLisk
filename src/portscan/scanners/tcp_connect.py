import asyncio 
from contextlib import suppress
from dataclasses import dataclass
from typing import Optional

@dataclass
class ProbeResult: 
    host: str
    port: int
    proto: str
    state: str
    banner: Optional[str] = None 
    reason: Optional[str] = None


