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
**Version 0.8.0**  
Copyright (c) 2025 FMNowacki  
A lightweight Python port scanner inspired by tools like Nmap.  
Built for learning and showcasing practical skills in **network security** and **Python**.

## Features

### Scanning Capabilities
- **TCP connect() scanning** - No root/Administrator privileges required
- **UDP scanning** - No root/Administrator privileges required
- **Service detection** - Identifies common services (HTTP, HTTPS, SSH, SMTP, FTP)
- **Banner grabbing** - Captures service banners for version detection

### Output Options
- **Human-readable text** output for quick analysis
- **Machine-friendly JSON** output for automation and parsing

### Performance & Control
- **Configurable port ranges** - Scan specific ports or ranges (`-p 1-1024,80,443`)
- **Top ports scanning** - Scan the most common ports (`--top 100`)
- **Adjustable timeouts** - Per-port connection timeout (`-to`)
- **Concurrency control** - Maximum concurrent probes (`-cc`)
- **Batch processing** - Process ports in batches for stability (`-b`)
- **Scan profiles** - Predefined timing profiles (`--profile {paranoid,normal,aggressive}`)

### Logging & Debugging (NEW in v0.8.0)
- **Debug mode** (`--debug`) - See detailed connection attempts, service probes, and errors
- **File logging** (`--log-file`) - Save complete scan logs for audit trails
- **Quiet mode** (`--quiet`) - Suppress banner and info messages for automation
- **Colored output** - Easy-to-read console output with color-coded log levels
- **Performance tracking** - Automatic timing of scan operations

## Pre-requisites

- Python **3.10+**

## Disclaimer ⚠️

This tool is for **educational purposes only**.  
**Do not** scan networks you do not own or have explicit permission to test.  
The author is not responsible for misuse of this software.

## Installation & Usage

### Installation

ReconLisk is used by downloading the repository and running it directly through Python:

```bash
git clone https://github.com/FMNowacki/ReconLisk.git
cd ReconLisk
```

### Basic Usage

```bash
# Basic TCP scan of common ports
python -m portscan.cli scanme.nmap.org -p 1-1024

# Scan specific ports
python -m portscan.cli 192.168.1.1 -p 22,80,443

# Scan top 100 most common ports
python -m portscan.cli 192.168.1.1 --top 100

# UDP scan
python -m portscan.cli 8.8.8.8 --scan udp -p 53,123,161
```

### Advanced Usage

```bash
# Debug mode - see all connection attempts
python -m portscan.cli scanme.nmap.org -p 1-1000 --debug

# Save logs to file
python -m portscan.cli 192.168.1.1 -p 1-5000 --log-file scan.log

# Quiet mode for scripting
python -m portscan.cli 192.168.1.1 -p 80,443 --quiet

# JSON output for parsing
python -m portscan.cli scanme.nmap.org -p 80,443 --json

# Aggressive scan profile
python -m portscan.cli 192.168.1.1 -p 1-1000 --profile aggressive

# Custom timing
python -m portscan.cli 192.168.1.1 -p 1-1000 -to 1.5 -cc 300 -b 1000

# Debug with file logging
python -m portscan.cli 192.168.1.1 -p 1-5000 --debug --log-file debug.log
```

## Command-Line Options

### Target & Scan Type
```
  host                    Hostname or IPv4 address to scan
  --scan {tcp,udp}        Type of scan to perform (default: tcp)
```

### Port Specification
```
  -p, --ports PORTS       Port specification, e.g '1-1024,80,443' (default: 1-1024)
  --top N                 Scan the top N most common TCP ports (overrides --ports)
```

### Timing & Performance
```
  -to, --timeout SECS     Connection timeout per port in seconds (default: 0.8)
  -cc, --concurrency N    Maximum concurrent probes (default: 500)
  -b, --batch N           Number of ports per batch (default: 2000)
  --profile PROFILE       Predefined timing profile: paranoid, normal, aggressive
```

### Output Options
```
  --json                  Output results in JSON format
```

### Logging & Debugging
```
  --debug                 Enable debug logging (shows all connection attempts)
  --log-file FILE         Write detailed logs to file
  -q, --quiet             Suppress banner and info messages (errors only)
```

### Other
```
  --version               Show version and exit
  -h, --help              Show help message and exit
```

## Scan Profiles

| Profile      | Timeout | Concurrency | Batch Size | Use Case                    |
|--------------|---------|-------------|------------|-----------------------------|
| `paranoid`   | 2.5s    | 100         | 200        | Stealthy, reliable scanning |
| `normal`     | 1.5s    | 250         | 500        | Balanced speed & accuracy   |
| `aggressive` | 1.0s    | 300         | 700        | Fast scanning               |

Individual timing flags (`-to`, `-cc`, `-b`) override profile settings.

## Output Examples

### Text Output (Default)
```
Scan Report for scanme.nmap.org (45.33.32.156)
22/tcp open  service: SSH  banner: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6
80/tcp open  service: HTTP  banner: HTTP/1.1 200 OK | Server: Apache/2.4.7

2 open ports found in 3.45s
```

### JSON Output
```json
{
  "target": "scanme.nmap.org",
  "ip": "45.33.32.156",
  "elapsed_seconds": 3.450,
  "results": [
    {
      "host": "45.33.32.156",
      "port": 22,
      "proto": "tcp",
      "state": "open",
      "banner": "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6",
      "reason": "connect-ok",
      "service": "SSH"
    },
    {
      "host": "45.33.32.156",
      "port": 80,
      "proto": "tcp",
      "state": "open",
      "banner": "HTTP/1.1 200 OK | Server: Apache/2.4.7",
      "reason": "connect-ok",
      "service": "HTTP"
    }
  ]
}
```

### Debug Output
```
DEBUG: Probing 45.33.32.156:22 (attempt 1/1)
DEBUG: Connected to 45.33.32.156:22
DEBUG: Banner from 45.33.32.156:22: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6
DEBUG: Attempting SSH probe on 45.33.32.156:22
DEBUG: Service detected on 45.33.32.156:22: SSH
DEBUG: Port 45.33.32.156:22 is OPEN
```

## Architecture

ReconLisk uses an asynchronous architecture built on Python's `asyncio` library:

- **Concurrent scanning** - Multiple ports scanned simultaneously with semaphore-based concurrency control
- **Batch processing** - Ports processed in configurable batches for memory efficiency
- **Non-blocking I/O** - Fully asynchronous network operations
- **Service detection** - Optional deep inspection of open ports with protocol-specific probes

## Supported Services

ReconLisk can detect the following services:

| Port(s)              | Service | Detection Method           |
|----------------------|---------|----------------------------|
| 21                   | FTP     | Banner grab + protocol     |
| 22                   | SSH     | Banner grab                |
| 25                   | SMTP    | Banner grab + EHLO command |
| 80, 8080, 8000, 8081 | HTTP    | HEAD request               |
| 443, 8443, 9443      | HTTPS   | TLS handshake + certificate|

Additional services detected through generic banner grabbing.

## Dependencies

This project is built entirely in **Python 3.10+** using only the standard library:
- `asyncio` - Asynchronous I/O
- `socket` - Network sockets
- `ssl` - TLS/SSL support
- `argparse` - Command-line parsing
- `json` - JSON output formatting
- `dataclasses` - Data structures

**No external dependencies required!**

## Exit Codes

| Code | Meaning                              |
|------|--------------------------------------|
| 0    | Success - scan completed normally    |
| 1    | DNS/hostname resolution failed       |
| 2    | Invalid port specification           |
| 3    | Scan failed (network error, etc.)    |
| 130  | User interrupted (Ctrl+C)            |

## Use Cases

- **Learning network security** - Understand how port scanners work
- **Network reconnaissance** - Discover open ports on your own systems
- **Service enumeration** - Identify running services and versions
- **Security auditing** - Test firewall rules and network exposure
- **Automation** - Integrate with scripts using JSON output and quiet mode

## Future Enhancements

- Two-phase architecture (separate port discovery from service detection)
- Additional service detection protocols
- IPv6 support
- SYN/Stealth scanning (requires root privileges)
- OS fingerprinting
- Scan result persistence and resumption
- Web-based UI

## Inspiration & Credits

This tool is inspired by **[Nmap](https://nmap.org/)** - the industry-standard network scanner.

ReconLisk is a learning project focused on understanding the fundamentals of network scanning, asynchronous programming, and Python software development.

## License

This project is licensed under the **BSD 3-Clause License** - see the [LICENSE](LICENSE) file for details.

## Contributing

This is a personal learning project, but suggestions and feedback are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Share your experience using ReconLisk

## Contact

**Author:** Filip Nowacki  
**GitHub:** [FMNowacki/ReconLisk](https://github.com/FMNowacki/ReconLisk)

---

**Remember:** Always obtain proper authorization before scanning networks. Unauthorized scanning may be illegal in your jurisdiction.