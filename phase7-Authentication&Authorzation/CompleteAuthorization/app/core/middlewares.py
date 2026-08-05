import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

def register_middlewares(app: FastAPI):
    
    app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React
        "http://localhost:8000",   # FastAPI direct
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

    @app.middleware("http")
    async def logging(
        request : Request,
        call_next,
    ):
        start_time = time.perf_counter()

        response = await call_next(request)
        
        process_time = time.perf_counter() - start_time
        
        logger.info(
            f"{request.method} {request.url.path} -> "
            f"{response.status_code} "
            f"({process_time * 1000:.2f} ms)"
        )
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        return response
    
    
        