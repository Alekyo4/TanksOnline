def call(dt: str | dict, status: bool = True) -> dict:
    return {
        "status": "ok" if status else "error",
        "data" if isinstance(dt, dict) else "detail": dt,
    }
