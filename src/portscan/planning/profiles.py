from dataclasses import dataclass

@dataclass(frozen=True)
class ScanProfile:
    timeout: float
    concurrency: int
    batch: int

#Profile settings 
PROFILES = {
    "paranoid": ScanProfile(timeout=2.0, concurrency=100, batch=300), 
    "normal": ScanProfile(timeout=0.8, concurrency=500, batch=1500),
    "aggressive": ScanProfile(timeout=0.5, concurrency=1500, batch=3000)
}

def resolve_profile(name: str | None, fallback: ScanProfile) -> ScanProfile:
    if not name:
        return fallback
    return PROFILES.get(name, fallback)