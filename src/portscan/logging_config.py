"""
Logging configuration for ReconLisk scanner.
Module provides centralized logging setup with support for:
- Console output with colored formatting
- Optional file logging
- Debug mode for detailed troubleshooting
- Performance timing logs
"""

import logging
import sys
from typing import Optional
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    #Custom formatter to add colors to log levels
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        if sys.stdout.isatty():  #Only colorize if outputting to terminal
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)


def setup_logging(
    debug: bool = False,
    log_file: Optional[Path] = None,
    quiet: bool = False
) -> logging.Logger:
    
    #Configgure logging for application
    """
    Args:
        debug: Enable debug-level logging
        log_file: Optional file path to write logs to
        quiet: Suppress all console output except errors
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("reconlisk")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    #Clears any existing handlers
    logger.handlers.clear()
    
    #Console handler
    if not quiet:
        console_handler = logging.StreamHandler(sys.stderr)
        
        if debug:
            console_handler.setLevel(logging.DEBUG)
            console_format = ColoredFormatter(
                '%(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
            )
        else:
            console_handler.setLevel(logging.INFO)
            console_format = ColoredFormatter(
                '%(levelname)s: %(message)s'
            )
        
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
    
    #File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        logger.info(f"Logging to file: {log_file}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    #Get a logger instance for a specific module
    """
    Args:
        name: Module name (usually __name__)
    Returns:
        Logger instance
    """
    return logging.getLogger(f"reconlisk.{name}")


#Convenience function for timing operations
class LogTimer:
    #Context manager for timing and logging operations
    
    def __init__(self, logger: logging.Logger, operation: str, level: int = logging.DEBUG):
        self.logger = logger
        self.operation = operation
        self.level = level
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.perf_counter()
        self.logger.log(self.level, f"Starting: {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        elapsed = time.perf_counter() - self.start_time
        if exc_type is None:
            self.logger.log(self.level, f"Completed: {self.operation} in {elapsed:.3f}s")
        else:
            self.logger.error(f"Failed: {self.operation} after {elapsed:.3f}s - {exc_type.__name__}: {exc_val}")
        return False  #Don't suppress exceptions