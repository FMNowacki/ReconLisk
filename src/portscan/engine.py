import asyncio
import time
from typing import Iterable, List, Tuple 
from .scanners.tcp_connect import TCPConnectScanner, ProbeResult

async def _bounded_probe(scanner: TCPConnectScanner, host: str, port: int, sem: asyncio.Semaphore):
    async with sem:
        return await scanner.probe(host, port)

#New Chuck Function to split task up
def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

#Redefined run_scan -> runs in batches now, more stable
async def run_scan(host: str, ports: Iterable[int], timeout: float, concurrency: int, batch_size: int = 2000) -> Tuple[List[ProbeResult]]:
    scanner = TCPConnectScanner(timeout=timeout)
    sem = asyncio.Semaphore(max(1, concurrency))
    port_list = list(ports)

    results: List[ProbeResult] = []
    t0 = time.perf_counter()

    try: 
        for batch in _chunks(port_list, batch_size):
            tasks = [_bounded_probe(scanner, host, p, sem) for p in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            for r in batch_results:
                if isinstance(r, Exception):
                    results.append(ProbeResult(host, -1, "tcp", "closed", reason=type(r).__name__))
                else:
                    results.append(r)

    except asyncio.CancelledError:
        raise
    except Exception:
        pass

    elapsed = time.perf_counter() - t0
    return results, elapsed 
    

