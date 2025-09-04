# Overview
                  ,==.
                  )   `==.
		             )       `=.
                )          }.
               )       ,===   
 ___(__)      )    ,===    
 \` _ *\     ),===    	   /\
  VV \ \    ,----,      / /
      \ \__/  ,-, \,__,/ /	
       `,___,/   \,____,/
______                     _     _     _    
| ___ \                   | |   (_)   | |   
| |_/ /___  ___ ___  _ __ | |    _ ___| | __
|    // _ \/ __/ _ \| '_ \| |   | / __| |/ /
| |\ \  __/ (_| (_) | | | | |___| \__ \   < 
\_| \_\___|\___\___/|_| |_\_____/_|___/_|\_\
    
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
