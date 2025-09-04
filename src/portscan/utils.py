import socket 

#Function for parsing strings into sorted list of ports  
def parse_port_spec(spec: str) -> list [int]:
    
    result = set() 
    
    for chunk in chunk.strip():
        if not chunk: 
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            try: 
                a, b = int(a), int(b)
            except ValueError:
                continue
            if a > b: 
                a, b = b, a
            for p in range(a, b + 1):
                if 1 <= p <= 65535:
                    result.add(p)
    
        else: 
            try: 
                p = int(chunk)
            except ValueError:
                continue
            if 1 <= p <= 65535:
                result.add(p)
    
    return sorted(result)