import asyncio
import ssl
from portscan.logging_config import get_logger

logger = get_logger(__name__)


async def probe_http(host: str, port: int, timeout: float = 0.5):
    logger.debug(f"Probing HTTP service on {host}:{port}")
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
            logger.debug(f"HTTP probe on {host}:{port}: No response data")
            return "HTTP", "No Response"
        
        text = data.decode(errors="ignore")
        lines = text.splitlines()
        first_line = lines[0] if lines else ""

        server_header = None
        for line in lines:
            if line.lower().startswith("server:"):
                server_header = line.strip()
                break
        
        if server_header:
            logger.debug(f"HTTP server on {host}:{port}: {first_line} | {server_header}")
            return "HTTP", f"{first_line} | {server_header}"
        else:
            logger.debug(f"HTTP server on {host}:{port}: {first_line or 'No Server Header'}")
            return "HTTP", first_line or "No Server Header"

    except asyncio.TimeoutError:
        logger.debug(f"HTTP probe timeout on {host}:{port}")
        return None, None
    except ConnectionResetError:
        logger.debug(f"HTTP probe connection reset on {host}:{port}")
        return None, None
    except Exception as e:
        logger.debug(f"HTTP probe failed on {host}:{port}: {type(e).__name__}: {e}")
        return None, None

    
async def probe_https(host: str, port: int, timeout: float = 0.7):
    logger.debug(f"Probing HTTPS service on {host}:{port}")
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
            logger.debug(f"HTTPS certificate on {host}:{port}: CN={common_name}")
            return "HTTPS", common_name
        
        logger.debug(f"HTTPS on {host}:{port}: No certificate info")
        return "HTTPS", None
    
    except asyncio.TimeoutError:
        logger.debug(f"HTTPS probe timeout on {host}:{port}")
        return None, None
    except ssl.SSLError as e:
        logger.debug(f"HTTPS SSL error on {host}:{port}: {e}")
        return None, None
    except ConnectionResetError:
        logger.debug(f"HTTPS probe connection reset on {host}:{port}")
        return None, None
    except Exception as e:
        logger.debug(f"HTTPS probe failed on {host}:{port}: {type(e).__name__}: {e}")
        return None, None


async def probe_ssh(host: str, port: int, timeout: float = 0.7):
    logger.debug(f"Probing SSH service on {host}:{port}")
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
            logger.debug(f"SSH probe on {host}:{port}: No banner received")
            return "SSH", "No Response"
        
        banner_str = banner.decode(errors="ignore").strip()
        logger.debug(f"SSH banner on {host}:{port}: {banner_str}")
        return "SSH", banner_str
    
    except asyncio.TimeoutError:
        logger.debug(f"SSH probe timeout on {host}:{port}")
        return None, None
    except ConnectionResetError:
        logger.debug(f"SSH probe connection reset on {host}:{port}")
        return None, None
    except Exception as e:
        logger.debug(f"SSH probe failed on {host}:{port}: {type(e).__name__}: {e}")
        return None, None

    
async def probe_smtp(host: str, port: int, timeout: float = 1.0):
    logger.debug(f"Probing SMTP service on {host}:{port}")
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
            logger.debug(f"SMTP probe on {host}:{port}: No response")
            return "SMTP", "No Response"
        
        result = " | ".join(parts)
        logger.debug(f"SMTP server on {host}:{port}: {result[:80]}{'...' if len(result) > 80 else ''}")
        return "SMTP", result
     
    except asyncio.TimeoutError:
        logger.debug(f"SMTP probe timeout on {host}:{port}")
        return None, None
    except ConnectionResetError:
        logger.debug(f"SMTP probe connection reset on {host}:{port}")
        return None, None
    except Exception as e:
        logger.debug(f"SMTP probe failed on {host}:{port}: {type(e).__name__}: {e}")
        return None, None


async def probe_ftp(host: str, port: int, timeout: float = 1.0):
    logger.debug(f"Probing FTP service on {host}:{port}")
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
            logger.debug(f"FTP probe on {host}:{port}: No banner received")
            return "FTP", "No Response"
        
        banner_str = banner.decode(errors="ignore").strip()
        logger.debug(f"FTP banner on {host}:{port}: {banner_str}")
        return "FTP", banner_str
    
    except asyncio.TimeoutError:
        logger.debug(f"FTP probe timeout on {host}:{port}")
        return None, None
    except ConnectionResetError:
        logger.debug(f"FTP probe connection reset on {host}:{port}")
        return None, None
    except Exception as e:
        logger.debug(f"FTP probe failed on {host}:{port}: {type(e).__name__}: {e}")
        return None, None