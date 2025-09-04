# Overview
<div align="center">
<pre>
                  ,==.
                  )   `==.
                 )       `=.
                )          }.
               )       ,===   
 ___(__)      )    ,===    
 \` _ *\     ),===         /\
  VV \ \    ,----,      / /
      \ \__/  ,-, \,__,/ / 
       `,___,/   \,____,/
______                     _     _     _    
| ___ \                   | |   (_)   | |   
| |_/ /___  ___ ___  _ __ | |    _ ___| | __
|    // _ \/ __/ _ \| '_ \| |   | / __| |/ /
| |\ \  __/ (_| (_) | | | | |___| \__ \   < 
\_| \_\___|\___\___/|_| |_\_____/_|___/_|\_\
</pre>
</div>

A lightweight, asyncio-based port scanner inspired by tools like Nmap.  
This project is built for learning and showcasing practical skills in network security and Python concurrency.  

## Features

- TCP connect() scanning (no root privileges required).

- Banner grabbing (best-effort, non-blocking).

- Human-readable text output or machine-friendly JSON output.

- Configurable:
  - Port ranges (-p 1-1024,80,443)
  - Timeout per connection
  - Maximum concurrency

 ## Pre-requisites 

 Python 3.10+ / Virtual Enviornement Recommended 

 ## Disclaimer ⚠️

This tool is for **educational purposes only**.
**Do not** scan networks you do not own or have explicit permission to test.
The author is not responsible for misuse of this software.

## Dependencies & Credits 

This project is built entirely in python 3.10+

### Libraries

asyncio - for asynchrenous I/O, enabling thousands of concurrent port probes without blocking (https://docs.python.org/3/library/asyncio.html)  
socket - for hostname resolution and low-level networking (https://docs.python.org/3/library/socket.html)  
dataclasses - to define simple and structured containers for scan resulst (https://docs.python.org/3/library/dataclasses.html)  
context.suppress - to ignore expected exceptions (https://docs.python.org/3/library/contextlib.html#contextlib.suppress)  
typing - for type hints (https://docs.python.org/3/library/typing.html)  

### Inspiration

This tool is inspired from Nmap (https://nmap.org/), an industry standard port scanner.   
