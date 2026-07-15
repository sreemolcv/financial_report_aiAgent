import time
from functools import wraps

def timed(label: str = ""):
    """Decorator to print how long a function took (useful for debugging
    PDF processing / embedding performance)."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            start = time.time()
            result = func(*args,**kwargs)
            elapsed = time.time() - start
            tag = label or func.__name__
            print(f"[timimg] {tag} took {elapsed:.2f}s")
            return result
        return wrapper
    return decorator

def truncate(text: str, max_chars: int = 300) -> str:
    """Truncate long text for logging/preview purposes."""
    return text if len(text) <= max_chars else text[:max_chars].rstrip() + "..."
