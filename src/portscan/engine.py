import asyncio
import time
from typing import Iterable, Tuple 
from .scanners.tcp_connect import TCPConnectScanner

async def _bounded_probe(scanner: TCPConnectScanner, host: str, port: int, sem: asyncio.Semaphore):
    async with sem:
        return await scanner.probe(host, port)
    
async def run_scan(host: str, ports: Iterable[int], timeout: float, concurrency: int) -> Tuple[list]:
    scanner = TCPConnectScanner(timeout=timeout)
    sem = asyncio.Semaphore(max(1, concurrency))
    port_list = list(ports)

    t0 = time.perf_counter()
    tasks = [_bounded_probe(scanner, host, p, sem) for p in port_list]
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - t0
    return results, elapsed 
    

