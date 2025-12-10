import asyncio, ssl

async def probe_http(host: str, port: int, timeout: float = 0.5):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        writer.write(b"HEAD / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
        await writer.drain()
        data = await asyncio.wait_for(reader.read(200), timeout)
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        if not data:
            return "HTTP", "No Response"
        
        text= data.decode(errors="ignore")
        lines= text.splitlines()
        first_line = lines[0] if lines else ""

        server_header = None
        for line in lines:
            if line.lower().startswith("server:"):
                server_header = line.strip()
                break
        
        if server_header:
            return "HTTP", f"{first_line} | {server_header}"
        else:
            return "HTTP", first_line or "No Server Header"

    except Exception:
        return None, None
    
async def probe_https(host: str, port: int, timeout: float = 0.7):
    ctx = ssl.create_default_context()
    try: 
        _reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port, ssl=ctx, server_hostname=host), timeout)
        try:
            ssl_object = writer.get_extra_info("ssl_object")
            certificate = ssl_object.getpeercert() if ssl_object else None
        finally: 
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass

        if certificate:
            subject = certificate.get("subject", [[("commonName", "Unknown")]])
            common_name = subject[0][0][1] if subject and subject[0] else "Unknown"
            return "HTTPS", common_name
        
        return "HTTPS", None
    
    except Exception:
        return None, None


async def probe_ssh(host: str, port: int, timeout: float = 0.7):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        try:
            banner = await asyncio.wait_for(reader.readline(), timeout)
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
        
        if not banner:
            return "SSH", "No Response"
        return "SSH", banner.decode(errors="ignore").strip()
    except Exception:
        return None, None   
    
async def probe_smtp(host: str, port: int, timeout: float = 1.0):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        try:
            banner = await asyncio.wait_for(reader.readline(), timeout)
            writer.write(b"EHLO example.com\r\n")
            await writer.drain()
            response = await asyncio.wait_for(reader.readline(), timeout)
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
        
        parts = []
        if banner:
            parts.append(banner.decode(errors="ignore").strip())
        if response:
            parts.append(response.decode(errors="ignore").strip())
        if not parts:
            return "SMTP", "No Response"
        return "SMTP", " | ".join(parts)
     
    except Exception:
        return None, None


async def probe_ftp(host: str, port: int, timeout: float = 1.0):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        try:
            banner = await asyncio.wait_for(reader.readline(), timeout)
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
        
        if not banner:
            return "FTP", "No Response"
        return "FTP", banner.decode(errors="ignore").strip()
    
    except Exception:
        return None, None