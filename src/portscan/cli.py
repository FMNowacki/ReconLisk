import argparse
import asyncio
import sys
import shutil

from datetime import datetime
from pathlib import Path
from portscan.logging_config import setup_logging, get_logger
from portscan.utils import parse_port_spec, resolve_host, top_ports
from portscan.planning.profiles import resolve_profile, ScanProfile
from portscan.engine import run_scan, run_scan_with
from portscan.scanners.udp_scan import UDPScanner
from portscan.output import formatters
from portscan.banner import ASCII_ART, DISCLAIMER
from portscan import __version__


def show_banner(ascii_art: str, disclaimer: str, version: str, quiet: bool = False):
    """Display the ASCII art banner and disclaimer."""
    if quiet:
        return  #Skip banner in quiet mode
    
    #Reflow artifacts avoidance
    print("\033[2J\033[H", end="")

    #Hide banner if terminal too narrow
    width = shutil.get_terminal_size((80, 24)).columns
    max_line = max(len(line.rstrip()) for line in ascii_art.splitlines())
    if max_line > width:
        print(f"ReconLisk v{version} - terminal too narrow to display banner\n")
    else:
        print(ascii_art.rstrip())
        print()
        print(f"ReconLisk v{version} - an asyncio based scanner")
        print("Copyright (c) 2025 FMNowacki")
    print(disclaimer)


def main() -> None:
    """Main entry point for ReconLisk port scanner."""
    ap = argparse.ArgumentParser(
        prog="reconlisk", 
        description="A lightweight asyncio-based TCP/UDP port scanner with service detection."
    )

    #Target and scan type
    ap.add_argument("host", help="Hostname or IPv4 address to scan")
    ap.add_argument(
        "--scan", 
        choices=["tcp", "udp"], 
        default="tcp", 
        help="Type of scan to perform (default: tcp)"
    )
    
    #Port specification
    ap.add_argument(
        "-p", "--ports", 
        default="1-1024", 
        help="Port specification, e.g '1-1024,80,443' (default: 1-1024)"
    )
    ap.add_argument(
        "--top", 
        type=int, 
        metavar="N",
        help="Scan the top N most common TCP ports (overrides --ports)"
    )
    
    #Timing and performance
    ap.add_argument(
        "-to", "--timeout", 
        type=float, 
        default=0.8, 
        help="Connection timeout per port in seconds (default: 0.8)"
    )
    ap.add_argument(
        "-cc", "--concurrency", 
        type=int, 
        default=500, 
        help="Maximum concurrent probes (default: 500)"
    )
    ap.add_argument(
        "-b", "--batch", 
        type=int, 
        default=2000, 
        help="Number of ports per batch (default: 2000)"
    )
    ap.add_argument(
        "--profile", 
        choices=["paranoid", "normal", "aggressive"], 
        help="Predefined timing profile (overrides individual timing options)"
    )
    
    #Output options
    ap.add_argument(
        "--json", 
        action="store_true", 
        help="Output results in JSON format"
    )
    
    #Logging options
    ap.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug logging (shows all connection attempts)"
    )
    ap.add_argument(
        "--log-file", 
        type=Path, 
        metavar="FILE",
        help="Write detailed logs to file"
    )
    ap.add_argument(
        "-q", "--quiet", 
        action="store_true", 
        help="Suppress banner and info messages (errors only)"
    )
    
    #Version
    ap.add_argument(
        "--version", 
        action="version", 
        version=f"ReconLisk {__version__}"
    )
    
    args = ap.parse_args()

    #Setup logging 
    logger = setup_logging(
        debug=args.debug, 
        log_file=args.log_file, 
        quiet=args.quiet
    )
    
    logger.info(f"ReconLisk v{__version__} starting")
    logger.debug(f"CLI arguments: {vars(args)}")
    
    #Show banner (respects quiet mode)
    start_time = datetime.now()
    show_banner(ASCII_ART, DISCLAIMER, __version__, quiet=args.quiet)
    
    #Log scan start
    if not args.quiet:
        print(f"Starting scan on {args.host} at {start_time:%Y-%m-%d %H:%M:%S}")
    logger.info(f"Starting scan on {args.host} at {start_time:%Y-%m-%d %H:%M:%S}")

    #Resolve target and ports
    target = args.host
    try:
        ip = resolve_host(target)
        logger.debug(f"Resolved {target} to {ip}")
    except Exception as e:
        logger.error(f"Failed to resolve host '{target}': {e}")
        print(f"Error: Could not resolve host '{target}'", file=sys.stderr)
        sys.exit(1)
    
    #Parse port specification
    if args.top:
        ports = top_ports(args.top)
        logger.debug(f"Using top {args.top} ports")
    else:
        ports = parse_port_spec(args.ports)
        logger.debug(f"Parsed port spec '{args.ports}' into {len(ports)} ports")

    if not ports:
        logger.error("No valid ports specified")
        print("Error: No valid ports specified", file=sys.stderr)
        sys.exit(2)

    #Resolve profile and timing parameters
    chosen = resolve_profile(
        args.profile, 
        ScanProfile(
            timeout=args.timeout, 
            concurrency=args.concurrency, 
            batch=args.batch
        )
    )
    timeout = chosen.timeout
    concurrency = chosen.concurrency
    batch = chosen.batch
    
    #Individual flags override profile
    if args.timeout != ap.get_default("timeout"):
        timeout = args.timeout
        logger.debug(f"Timeout overridden to {timeout}s")
    if args.concurrency != ap.get_default("concurrency"):
        concurrency = args.concurrency
        logger.debug(f"Concurrency overridden to {concurrency}")
    if args.batch != ap.get_default("batch"):
        batch = args.batch
        logger.debug(f"Batch size overridden to {batch}")
    
    logger.info(f"Scan configuration: {args.scan.upper()} scan, {len(ports)} ports, "
                f"timeout={timeout}s, concurrency={concurrency}, batch={batch}")

    #Run the scan
    try:
        if args.scan == "udp":
            logger.debug("Creating UDP scanner")
            scanner = UDPScanner(
                timeout=timeout,
                retries=getattr(chosen, "retries", 0),
                retry_delay=getattr(chosen, "retry_delay", 0.2),
            )
            results, elapsed = asyncio.run(
                run_scan_with(scanner, ip, ports, concurrency=concurrency, batch_size=batch)
            )
        else:
            #Default TCP connect scan
            logger.debug("Creating TCP connect scanner")
            results, elapsed = asyncio.run(
                run_scan(
                    ip,
                    ports,
                    timeout=timeout,
                    concurrency=concurrency,
                    batch_size=batch,
                    retries=getattr(chosen, "retries", 0),
                    retry_delay=getattr(chosen, "retry_delay", 0.2),
                )
            )
    except KeyboardInterrupt:
        logger.warning("Scan interrupted by user")
        print("\nScan interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        logger.error(f"Scan failed: {type(e).__name__}: {e}")
        print(f"Error: Scan failed - {e}", file=sys.stderr)
        sys.exit(3)

    end_time = datetime.now()
    
    #Output results
    if args.json:
        print(formatters.to_json(target, ip, results, elapsed))
    else:
        print(formatters.to_text(target, ip, results, elapsed))
    
    #Log completion
    if not args.quiet:
        print(f"Scan finished at {end_time:%Y-%m-%d %H:%M:%S}")
    logger.info(f"Scan finished at {end_time:%Y-%m-%d %H:%M:%S}")


if __name__ == "__main__":
    main()