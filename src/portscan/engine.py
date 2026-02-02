import asyncio
import logging
import time
from typing import Iterable, List, Tuple, Protocol
from portscan.logging_config import get_logger, LogTimer
from .scanners.tcp_connect import TCPConnectScanner, ProbeResult

logger = get_logger(__name__)


class Scanner(Protocol):
    async def probe(self, host: str, port: int) -> ProbeResult: ...


async def _bounded_probe(scanner: Scanner, host: str, port: int, sem: asyncio.Semaphore) -> ProbeResult:
    """Execute a probe with semaphore-based concurrency control."""
    async with sem:
        return await scanner.probe(host, port)


def _chunks(seq: List[int], n: int) -> Iterable[List[int]]:
    """Split a sequence into chunks of size n."""
    for i in range(0, len(seq), n):
        yield seq[i:i+n]


async def run_scan_with(
    scanner: Scanner, 
    host: str, 
    ports: Iterable[int], 
    concurrency: int, 
    batch_size: int = 2000
) -> Tuple[List[ProbeResult], float]:
    #Run a port scan using the provided scanner.
    """
    Args:
        scanner: Scanner implementation to use
        host: Target host IP address
        ports: Iterable of ports to scan
        concurrency: Maximum concurrent probes
        batch_size: Number of ports to process per batch
    Returns:
        Tuple of (results list, elapsed time in seconds)
    """
    eff_concurrency = max(1, min(concurrency, batch_size))
    sem = asyncio.Semaphore(eff_concurrency)
    port_list = list(ports)
    results: List[ProbeResult] = []
    t0 = time.perf_counter()
    
    logger.info(f"Starting scan of {len(port_list)} ports on {host}")
    logger.debug(f"Scan parameters: concurrency={eff_concurrency}, batch_size={batch_size}")

    with LogTimer(logger, f"Scanning {len(port_list)} ports on {host}", level=logging.INFO):
        try:
            for batch_num, batch in enumerate(_chunks(port_list, batch_size), 1):
                logger.debug(f"Processing batch {batch_num}: ports {batch[0]}-{batch[-1]} ({len(batch)} ports)")
                
                tasks = [_bounded_probe(scanner, host, p, sem) for p in batch]
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Track statistics for this batch
                batch_open = 0
                batch_failed = 0
                
                # Process results - proper exception logging instead of just dropping them silently
                for idx, r in enumerate(batch_results):
                    if isinstance(r, ProbeResult):
                        results.append(r)
                        if r.state == "open":
                            batch_open += 1
                    elif isinstance(r, Exception):
                        batch_failed += 1
                        port = batch[idx]
                        logger.debug(f"Probe failed for {host}:{port} - {type(r).__name__}: {r}")
                        
                        # Include full traceback in debug mode for unexpected errors
                        if logger.isEnabledFor(logging.DEBUG) and not isinstance(r, (asyncio.TimeoutError, ConnectionRefusedError, OSError)):
                            import traceback
                            logger.debug(f"Traceback for {host}:{port}:\n{traceback.format_exception(type(r), r, r.__traceback__)}")
                
                # Log batch completion stats
                if batch_open > 0 or logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f"Batch {batch_num} complete: {batch_open} open, {batch_failed} failed")
                            
        except asyncio.CancelledError:
            logger.warning("Scan cancelled by user")
            raise
        except KeyboardInterrupt:
            logger.warning("Scan interrupted by user (Ctrl+C)")
            raise
        except Exception as e:
            logger.error(f"Scan failed with unexpected error: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            raise
        finally:
            elapsed = time.perf_counter() - t0
            open_ports = sum(1 for r in results if r.state == "open")
            logger.info(f"Scan completed: {open_ports}/{len(results)} open ports in {elapsed:.2f}s")
    
    return results, elapsed


async def run_scan(
    host: str, 
    ports: Iterable[int], 
    timeout: float, 
    concurrency: int, 
    batch_size: int = 2000, 
    retries: int = 0, 
    retry_delay: float = 0.2
) -> Tuple[List[ProbeResult], float]:
    #Run a TCP connect scan on the specified host and ports.
    """
    Args:
        host: Target host IP address
        ports: Iterable of ports to scan
        timeout: Connection timeout in seconds
        concurrency: Maximum concurrent probes
        batch_size: Number of ports to process per batch
        retries: Number of retry attempts for failed probes
        retry_delay: Delay between retries in seconds
    Returns:
        Tuple of (results list, elapsed time in seconds)
    """
    logger.debug(f"Creating TCPConnectScanner: timeout={timeout}s, retries={retries}, retry_delay={retry_delay}s")
    scanner = TCPConnectScanner(
        timeout=timeout, 
        retries=retries, 
        retry_delay=retry_delay
    )
    return await run_scan_with(scanner, host, ports, concurrency=concurrency, batch_size=batch_size)