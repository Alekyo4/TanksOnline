from fastapi import FastAPI
from uvicorn import run as uvicorn

from tanksonline.route import router as routers

app: FastAPI = FastAPI(title="TanksOnline", docs_url=None, redoc_url=None)

app.include_router(routers)


def main() -> None:
    uvicorn("tanksonline.main:app", host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    main()
