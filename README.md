# Overview
<div align="center">
<pre>
       ,==.       ,==.
       )   `==.   )   `==.
        )      `=)       `=.
         )      )          }.
          )    )       ,===   
 __(__)    )  )    ,===    
 \` _ *\     ),===       /\
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
Version 0.2.5<br>
Copyright (c) 2025 FNowacki<br>
A lightweight, **asyncio-based** port scanner inspired by tools like Nmap.  
Built for learning and for showcasing practical skills in **network security** and **Python concurrency**.  

## Features
- TCP **connect()** scanning (no root/Administrator privileges required)  
- Best-effort **banner grabbing** after successful connects  
- Human-readable **text** output and machine-friendly **JSON**  
- Configurable:  
  - Port ranges(`-p 1-1024,80,443`)  
  - Per-port timeout (`-t`)  
  - Maximum concurrency (`-c`)  
  - Top common ports (`--top N`)  
  - Scan profiles (`--profile {paranoid,normal,aggressive}`)  

 ## Pre-requisites 

- Python **3.10+**  
- A **virtual environment** is recommended  

 ## Disclaimer ⚠️

This tool is for **educational purposes only**.
**Do not** scan networks you do not own or have explicit permission to test.
The author is not responsible for misuse of this software.

## Installation & Usage

ReconLisk can be used in two ways:  

### 1. Run Directly with Python 

1. Clone repository
2. Run Scanner with: python -m portscan.cli

### 2. Install as a CLI app 

1. pip install e 
2. Run Scanner with: reconlisk

## Dependencies & Credits 

This project is built entirely in python 3.10+

### Standard Library Modules

- [`asyncio`](https://docs.python.org/3/library/asyncio.html)  
  For asynchronous I/O, enabling thousands of concurrent port probes without blocking.

- [`socket`](https://docs.python.org/3/library/socket.html)  
  For hostname resolution and low-level networking primitives.

- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)  
  To define simple, structured containers for scan results.

- [`contextlib.suppress`](https://docs.python.org/3/library/contextlib.html#contextlib.suppress)  
  To gracefully ignore expected exceptions (e.g., connection resets).

- [`typing`](https://docs.python.org/3/library/typing.html)  
  For type hints, improving clarity and IDE support.

- [`argparse`](https://docs.python.org/3/library/argparse.html)  
  For parsing command-line arguments.

- [`sys`](https://docs.python.org/3/library/sys.html)  
  For interacting with interpreter internals (e.g., `sys.exit`).

- [`time`](https://docs.python.org/3/library/time.html)  
  For measuring elapsed time during scans.

- [`datetime`](https://docs.python.org/3/library/datetime.html)  
  For human-readable scan start/end timestamps.

- [`json`](https://docs.python.org/3/library/json.html)  
  For machine-friendly JSON and JSONL output formats.


### Inspiration

This tool is inspired from Nmap (https://nmap.org/), an industry standard port scanner.   
