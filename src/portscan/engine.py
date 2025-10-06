import asyncio
import time
from typing import Iterable, List, Tuple, Protocol
from .scanners.tcp_connect import TCPConnectScanner, ProbeResult


class Scanner(Protocol):
    async def probe(self, host: str, port: int) -> ProbeResult: ...

async def _bounded_probe(scanner: Scanner, host: str, port: int, sem: asyncio.Semaphore):
    async with sem:
        return await scanner.probe(host, port)

#New Chuck Function to split task up
def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

async def run_scan_with(scanner: Scanner, host: str, ports: Iterable[int], concurrency: int, batch_size: int = 2000) -> Tuple[List[ProbeResult], float]:
    eff_concurrency = max(1, min(concurrency, batch_size))
    sem = asyncio.Semaphore(eff_concurrency)
    port_list = list(ports)
    results: List[ProbeResult] = []
    t0 = time.perf_counter()

    try:
        for batch in _chunks(port_list, batch_size):
            tasks = [_bounded_probe(scanner, host, p, sem) for p in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Keep only successful ProbeResult objects; skip exceptions (or log if you add --debug)
            for r in batch_results:
                if isinstance(r, ProbeResult):
                    results.append(r)
                # else: it's an Exception; skip or handle as you like
    except asyncio.CancelledError:
        raise
    finally:
        elapsed = time.perf_counter() - t0

    return results, elapsed
    


#Redefined run_scan -> runs in batches now, more stable
async def run_scan(host: str, ports: Iterable[int], timeout: float, concurrency: int, batch_size: int = 2000, retries: int = 0, retry_delay: float = 0.2) -> Tuple[List[ProbeResult], float]:
    scanner = TCPConnectScanner(timeout=timeout, retries=retries, retry_delay=retry_delay)
    return await run_scan_with(scanner, host, ports, concurrency=concurrency, batch_size=batch_size)
    

