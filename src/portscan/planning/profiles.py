from dataclasses import dataclass

@dataclass(frozen=True)
class ScanProfile:
    timeout: float
    concurrency: int
    batch: int

PROFILES = {
    "paranoid": ScanProfile(timeout=2.0, concurrency=200, batch=800), 
    "normal": ScanProfile(timeout=1.0, concurrency=500, batch=1500),
    "aggressive": ScanProfile(timeout=0.5, concurrency=1200, batch=3000)
}

def resolve_profile(name: str | None, fallback: ScanProfile) -> ScanProfile:
    if not name:
        return fallback
    return PROFILES.get(name, fallback)