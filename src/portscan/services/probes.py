import asyncio, ssl

async def probe_http(host: str, port: int, timeout: float = 0.5):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        writer.write(b"HEAD / HTTP/1.0\r\nHost: {}\r\n\r\n" % host.encode())
        await writer.drain()
        data = await asyncio.wait_for(reader.read(200), timeout)
        writer.close()
        await writer.wait_closed()
        if b"Server:" in data:
            return "HTTP", data.decode(errors="ignore").splitlines()[0]
        return "HTTP", "No Server Header"
    except Exception:
        return None, None
    
