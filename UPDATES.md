# ReconLisk Updates & Changelog

All notable changes to ReconLisk will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.8.0] - 2025-02-02

### Major Features

#### Comprehensive Logging System
- **Added** complete logging infrastructure with `logging_config.py`
- **Added** `--debug` flag to enable detailed connection logging
- **Added** `--log-file` flag to save logs to file for audit trails
- **Added** `--quiet` flag to suppress banner and info messages for automation
- **Added** colored console output for better readability
- **Added** automatic performance timing with `LogTimer` class

#### Enhanced Debugging
- **Added** logging to all scanner modules (`tcp_connect.py`, `udp_scan.py`)
- **Added** logging to all service probe functions (`probes.py`)
- **Added** detailed batch processing logs in `engine.py`
- **Added** visibility into every connection attempt, timeout, and failure

### Bug Fixes

#### Critical Fixes
- **Fixed** silent exception swallowing in `engine.py` that made debugging impossible
- **Fixed** missing `logging` module import that would have caused `NameError` at runtime
- **Fixed** banner timeout being too short (0.1s → 0.5s), causing missed service banners

#### Exception Handling
- **Improved** exception handling with specific error types instead of generic `Exception`
- **Added** differentiation between `TimeoutError`, `ConnectionRefusedError`, `OSError`, and `SSLError`
- **Fixed** retry logic to avoid unnecessary retries on refused connections and network errors

### Performance Improvements

- **Optimized** retry logic - only timeout errors trigger retries now
- **Improved** banner timeout from 0.1s to 0.5s for better service capture
- **Added** batch statistics showing open/failed ports per batch
- **Added** smarter traceback logging (only for unexpected errors)

### Improvements

#### CLI Enhancements
- **Added** better error messages with proper exit codes (0, 1, 2, 3, 130)
- **Added** DNS resolution error handling with clear user feedback
- **Added** keyboard interrupt (Ctrl+C) handling with graceful shutdown
- **Improved** help text for all command-line arguments
- **Added** errors now go to stderr instead of stdout (proper Unix behavior)

#### Code Quality
- **Added** comprehensive docstrings to all major functions
- **Added** type hints to previously untyped functions
- **Improved** code organization and readability
- **Added** detailed comments explaining complex logic

#### Service Detection
- **Improved** HTTP probe to capture both status line and Server header
- **Improved** HTTPS probe to extract certificate common name
- **Improved** SSH probe to capture full banner string
- **Improved** SMTP probe to send EHLO and capture response
- **Improved** FTP probe banner capture
- **Added** specific exception handling for SSL errors in HTTPS probes

#### Engine & Scanning
- **Added** batch progress logging with port ranges
- **Added** scan configuration summary logging
- **Added** final statistics showing open/total port ratio
- **Improved** error reporting with traceback support for fatal errors

### 📚 Documentation

- **Updated** README.md with comprehensive feature documentation
- **Added** UPDATES.md changelog file (this file)
- **Added** detailed logging usage examples
- **Added** exit code documentation
- **Added** scan profile comparison table
- **Added** output format examples (text, JSON, debug)
- **Added** architecture overview section

### 🔄 Internal Changes

- **Refactored** logging initialization to be centralized
- **Added** `get_logger()` function for module-level loggers
- **Added** `LogTimer` context manager for operation timing
- **Improved** batch processing with better error tracking
- **Added** configuration validation and logging

---


## Roadmap

### Planned for v0.9.0 - Two-Phase Architecture
- [ ] Separate port discovery from service detection
- [ ] Add `-sV` flag for optional service detection
- [ ] Add `--version-intensity` for detection depth control
- [ ] Faster initial scans (skip service detection by default)
- [ ] Ability to rerun service detection on saved results

### Planned for v1.0.0 - Production Ready
- [ ] IPv6 support
- [ ] OS fingerprinting (TTL-based)
- [ ] Host discovery (ping sweep)
- [ ] Additional service detection protocols
- [ ] Scan state persistence and resumption
- [ ] Rate limiting options
- [ ] Output to multiple formats simultaneously

### Future Considerations
- SYN/Stealth scanning (requires root)
- Parallel host scanning
- Web-based UI
- Report generation
- Integration with vulnerability databases
- Plugin system for custom service probes

---

## Version History Summary

| Version | Date       | Highlights                                    |
|---------|------------|-----------------------------------------------|
| 0.8.0   | 2025-02-02 | Logging system, bug fixes, better debugging   |


---

## Feedback & Bug Reports

Found a bug? Have a feature request? Please:
1. Check the [GitHub Issues](https://github.com/FMNowacki/ReconLisk/issues) page
2. Open a new issue with:
   - ReconLisk version (`--version`)
   - Python version (`python --version`)
   - Operating system
   - Command used
   - Expected vs actual behavior
   - Debug output (`--debug --log-file debug.log`)

---

## Contributors

- **Filip Nowacki** (@FMNowacki) - Original author and maintainer

Thank you to everyone who can provide feedback and suggestions!

---

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.