import argparse
import asyncio
import sys

from portscan.utils import parse_port_spec, resolve_host, top_ports
from portscan.planning.profiles import resolve_profile, ScanProfile
from portscan.engine import run_scan
from portscan.output import formatters

#Main Method 
def main() -> None:
    ap = argparse.ArgumentParser(prog="portscan", description="A lightweight asyncio-based TCP port scanner.")

    #All Command arguments
    ap.add_argument("host", help="Hostname or IPv4 address to scan")
    ap.add_argument("-p", "--ports", default="1-1024", help="Port spec, e.g '1-1024, 80, 443' (default: 1-1024)")
    ap.add_argument("--top", type=int, help="Scans some of the most common TCP ports (overrides --ports)")
    ap.add_argument("-to", "--timeout", type=float, default=0.8, help="Per-port connect timeout")
    ap.add_argument("-cc", "--concurrency", type=int, default=500, help="Max concurrent probes")
    ap.add_argument("--profile", choices=["paranoid", "normal", "aggressive"], help="Predefined aggression profiles")
    ap.add_argument("-b", "--batch", type=int, default=2000, help="Ports scheduled per batch (default: 2000)")
    ap.add_argument("--json", action="store_true", help="Output JSON instead of text")
    
    args = ap.parse_args()

    target = args.host
    ip = resolve_host(target)
    ports = top_ports(args.top) if args.top else parse_port_spec(args.ports)

    if not ports:
        print("No valid ports specified.")
        sys.exit(2)
    
    if args.timeout != ap.get_default("timeout"):
        timeout = args.timeout
    if args.concurrency != ap.get_default("concurrency"):
        concurrency = args.concurrency
    if args.batch != ap.get_default("batch"):
        batch = args.batch

    results, elapsed = asyncio.run(run_scan(ip, ports, timeout=args.timeout, concurrency=args.concurrency))

    #Output check
    if args.json: 
        print(formatters.to_json(target, ip, results, elapsed))
    else: 
        print(formatters.to_text(target, ip, results, elapsed))

if __name__ == "__main__":
    main()
