import socket 

COMMON_TCP = [
    80, 443, 22, 21, 25, 110, 143, 53, 3306, 3389, 5900, 8080,
    6379, 5432, 9200, 27017, 25, 587, 993, 995, 389, 636, 135,
    139, 445, 902, 912, 2049, 1723, 1521, 5000, 8000, 8443
]

def top_ports(n: int) -> list[int]:
    n = max(1, min(n, len(COMMON_TCP)))
    return COMMON_TCP[:n]

#Function for parsing strings into sorted list of ports  
def parse_port_spec(spec: str) -> list [int]:
    
    if not spec:
        return []
    
    ports: set[int] = set()

    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            try:
                a_str, b_str = part.split("-", 1)
                a, b = int(a_str), int(b_str)
            except ValueError:
                continue
            if a > b:
                a, b = b, a
            for p in range(a, b + 1):
                if 1 <= p <= 65535:
                    ports.add(p)
        else:
            try:
                p = int(part)
            except ValueError:
                continue
            if 1 <= p <= 65535:
                ports.add(p)

    return sorted(ports)

#Function to resolve a hostname to IPv4 address
def resolve_host(host: str) -> str:
    return socket.gethostbyname(host)