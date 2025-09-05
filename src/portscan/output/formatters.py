from typing import List
from ..scanners.tcp_connect import ProbeResult

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

