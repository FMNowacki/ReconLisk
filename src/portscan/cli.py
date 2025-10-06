import argparse
import asyncio
import sys
import shutil

from datetime import datetime
from portscan.utils import parse_port_spec, resolve_host, top_ports
from portscan.planning.profiles import resolve_profile, ScanProfile
from portscan.engine import run_scan, run_scan_with
from portscan.scanners.udp_scan import UDPScanner
from portscan.output import formatters
from portscan.banner import ASCII_ART, DISCLAIMER
from portscan import __version__

def show_banner(ascii_art: str, disclaimer: str, version: str):
    #reflow artifacts avoidance
    print("\033[2J\033[H", end="")

    #hide banner if terminal too narrow
    width = shutil.get_terminal_size((80, 24)).columns
    max_line = max(len(line.rstrip()) for line in ascii_art.splitlines())
    if max_line > width:
        print(f"ReconLisk v{version} - terminal too narrow to display banner\n")
    else:
        print(ascii_art.rstrip())
        print()
        print(f"ReconLisk v{version} - asyncio based scanner")
        print("Copyright (c) 2025 FMNowacki")
    print(disclaimer)

#Main Method 
def main() -> None:
    ap = argparse.ArgumentParser(prog="portscan", description="A lightweight asyncio-based TCP port scanner.")

    #All Command arguments
    ap.add_argument("--version", action="version", version=f"ReconLisk {__version__}")
    ap.add_argument("host", help="Hostname or IPv4 address to scan")
    ap.add_argument("--scan", choices=["tcp", "udp"], default="tcp", help="Type of scan to perform (default: connect/tcp).")
    ap.add_argument("-p", "--ports", default="1-1024", help="Port specification, e.g '1-1024, 80, 443' (default: 1-1024).")
    ap.add_argument("--top", type=int, help="Scans some of the most common TCP ports (overrides --ports)")
    ap.add_argument("-to", "--timeout", type=float, default=0.8, help="The maximum timeout for every port.")
    ap.add_argument("-cc", "--concurrency", type=int, default=500, help="The maximum number of concurrent probes.")
    ap.add_argument("--profile", choices=["paranoid", "normal", "aggressive"], help="Predefined aggression profiles.")
    ap.add_argument("-b", "--batch", type=int, default=2000, help="Number of ports scheduled per batch (default: 2000).")
    ap.add_argument("--json", action="store_true", help="Output JSON instead of text.")
    
    args = ap.parse_args()

    #Banner art and text
    start_time = datetime.now()
    show_banner(ASCII_ART, DISCLAIMER, __version__)
    print(f"Starting Scan on {args.host} at {start_time:%Y-%m-%d %H:%M:%S}...")

    #resolve target and ports
    target = args.host
    ip = resolve_host(target)
    ports = top_ports(args.top) if args.top else parse_port_spec(args.ports)

    if not ports:
        print("No valid ports specified.")
        sys.exit(2)

    #set profile
    chosen = resolve_profile( args.profile, ScanProfile(timeout=args.timeout, concurrency=args.concurrency, batch=args.batch))
    timeout = chosen.timeout
    concurrency = chosen.concurrency
    batch = chosen.batch
    
    #tuning flags override any profile
    if args.timeout != ap.get_default("timeout"):
        timeout = args.timeout
    if args.concurrency != ap.get_default("concurrency"):
        concurrency = args.concurrency
    if args.batch != ap.get_default("batch"):
        batch = args.batch

    
    #Build scanner and run appropriate runner
    if args.scan == "udp":
        scanner = UDPScanner(
            timeout=timeout,
            retries=getattr(chosen, "retries", 0),
            retry_delay=getattr(chosen, "retry_delay", 0.2),
        )
        results, elapsed = asyncio.run(
            run_scan_with(scanner, ip, ports, concurrency=concurrency, batch_size=batch)
        )
    else:
        # default TCP connect flow (backwards compatible)
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

    end_time = datetime.now()
    #Output check
    if args.json: 
        print(formatters.to_json(target, ip, results, elapsed))
    else: 
        print(formatters.to_text(target, ip, results, elapsed))
    print(f"Scan finished at {end_time:%Y-%m-%d %H:%M:%S}.")


if __name__ == "__main__":
    main()
