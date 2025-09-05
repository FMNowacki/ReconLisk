import json
from typing import List
from ..scanners.tcp_connect import ProbeResult

#Simple function to translate result to text
def to_text(target: str, ip: str, results: List[ProbeResult], elapsed: float) -> str:
    lines = [f"Scan Report for {target} ({ip})"]
    for r in sorted(results, key=lambda x: x.port):
        if r.state == "open":
            line = f"{r.port}/{r.proto} open"
            if r.banner:
                line += f"  banner: {r.banner[:80]}"
            lines.append(line)

    open_count = sum(1 for r in results if r.state == "open")
    lines.append(f"\n{open_count} open ports found in {elapsed:.2f}s")
    return "\n".join(lines)

#Simple function to translate reult to a json file
def to_json(target: str, ip: str, results: List[ProbeResult], elapsed: float) -> str:
    payload = {
        "target": target,
        "ip": ip,
        "elapsed_seconds": round(elapsed, 3),
        "results": [r.__dict__ for r in results],
    }
    return json.dumps(payload, indent=2)