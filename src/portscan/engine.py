import asyncio
from .scanners.tcp_connect import TCPConnectScanner, ProbeResult

async def _bounded_probe(scanner: TCPConnectScanner, host: str, port: int, sem: asyncio.Semaphore):
    async with sem:
        return await scanner.probe(host, port)
    

