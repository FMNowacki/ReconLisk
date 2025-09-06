import argparse
import asyncio
from portscan.utils import parse_port_spec, resolve_host
from portscan.engine import run_scan
from portscan.output import formatters

def main() -> None:
    ap = argparse.ArgumentParser(prog="portscan", description="A lightweight asyncio-based TCP port scanner.")
    ap.add_argument("host", help="Hostname or IPv4 address to scan")
    ap.add_argument("-p", "--ports", default="1-1024", help="Port spec, e.g '1-1024, 80, 443' (default: 1-1024)")
    ap.add_argument("-to", "--timeout", type=float, default=0.8, help="Per-port connect timeout")
    ap.add_argument("-cc", "--concurrency", type=int, default=500, help="Max concurrent probes")
    ap.add_argument("--json", action="store_true", help="Output JSON instead of text")

    args = ap.parse_args()

    target = args.host
    ip = resolve_host(target)
    ports = parse_port_spec(args.ports)

    results, elapsed = asyncio.run(run_scan(ip, ports, timeout=args.timeout, concurrency=args.concurrency))

    if args.json: 
        print(formatters.to_json(target, ip, results, elapsed))
    else: 
        print(formatters.to_text(target, ip, results, elapsed))

if __name__ == "__main__":
    main()
