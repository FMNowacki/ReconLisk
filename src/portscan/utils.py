import socket 

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