# Overview
```text
                                            .:=+*=-.
  -*########**=:                         :+###*:
     .+******#####*-. .-               =*##***:
      :++++******####*-:+.          .-*##****+-
     .+***#############**-         -+#########*+-
    -###***********###%**.        =*####****-
   .   .=+++++++**####*#        :**%####*++.
         =+++***#####*#-      :+**%##***##=
         -***##****#*##:     =***####**+++*
         =*#******#####=    :****###*=.   .
        -#***+++***###*#****###*###*.
       :-      =***##%#**###***#+. .
                =##%%%%#**##*****=:-
              .+#########**#***##***+:
             -*#*****#**###########***+-.
            :******##**#%########*****++-
            =*****###***++-.  .+**#******+.
           .+#****+.+***+:      -+*##+ -=-
           .*#****:   .+**++*=.   :*#*-
            =#****-    -**##+:.    .+*-:-.
            .*#****:   +:  -.-.         .:.:.
             .###*+**-..:                 ::
               -*##*********++-:.
                 .-+*#####****#**=
                               :*#-
                       -+.     -*#
                         .-+***=:

______                     _     _     _
| ___ \                   | |   (_)   | |
| |_/ /___  ___ ___  _ __ | |    _ ___| | __
|    // _ \/ __/ _ \| '_ \| |   | / __| |/ /
| |\ \  __/ (_| (_) | | | | |___| \__ \   <
\_| \_\___|\___\___/|_| |_\_____/_|___/_|\_\
```
Version 0.7.5<br>
Copyright (c) 2025 FMNowacki<br>
A lightweight python port scanner inspired by tools like Nmap.
Built for learning and for showcasing practical skills in **network security** and **Python**.

## Features
- TCP **connect()** scanning (no root/Administrator privileges required)
- UDP scanning (no root/Administrator privileges required)
- Best-effort **banner grabbing** after successful connects
- Human-readable **text** output and machine-friendly **JSON**
- Configurable:
  - Scans (`--scan {tcp, udp}`)
  - Port ranges(`-p 1-1024,80,443`)
  - Per-port timeout (`-t`)
  - Maximum concurrency (`-c`)
  - Top common ports (`--top N`)
  - Scan profiles (`--profile {paranoid,normal,aggressive}`)

 ## Pre-requisites

- Python **3.10+**

 ## Disclaimer ⚠️

This tool is for **educational purposes only**.
**Do not** scan networks you do not own or have explicit permission to test.
The author is not responsible for misuse of this software.

## Installation & Usage

Reconlisk is used through downloading the repository into a folder and then running it directly through python. <br>
An example command line would be (from project root): python -m portscan.cli 1.2.3.4 --scan udp -p 53,123 --profile paranoid<br>

## Dependencies & Credits

This project is built entirely in python 3.10+

### Inspiration

This tool is inspired from Nmap (https://nmap.org/).
