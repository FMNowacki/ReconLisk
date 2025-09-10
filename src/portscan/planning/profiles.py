from dataclasses import dataclass

@dataclass(frozen=True)
class ScanProfile:
    timeout: float
    concurrency: int
    batch: int
    retries: int = 0
    retry_delay: float = 0.2

#Profile settings 
PROFILES = {
    "paranoid": ScanProfile(timeout=2.5, concurrency=100, batch=200, retries=1, retry_delay=0.3), 
    "normal": ScanProfile(timeout=1.5, concurrency=250, batch=500, retries=1, retry_delay=0.2),
    "aggressive": ScanProfile(timeout=1, concurrency=300, batch=700, retries=1, retry_delay=0.1)
}

def resolve_profile(name: str | None, fallback: ScanProfile) -> ScanProfile:
    if not name:
        return fallback
    return PROFILES.get(name, fallback)