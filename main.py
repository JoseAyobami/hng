from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import httpx
import logging
from datetime import datetime
import os
import uvicorn


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


app = FastAPI(title="Profile API")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/me")
@limiter.limit("10/minute")
async def get_profile(request: Request):
    logger.info(f"Incoming request from {request.client.host}")
    
    current_time = datetime.utcnow().isoformat() + "Z"

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(
                "https://catfact.ninja/fact",
                params={"t": datetime.utcnow().timestamp()}
            )
            response.raise_for_status()
            cat_fact = response.json().get("fact", "No fact found")

        data = {
            "status": "success",
            "user": {
                "email": "bamjoe464@gmail.com",
                "name": "Joseph Ayeni",
                "stack": "Python/FastAPI"
            },
            "timestamp": current_time,
            "fact": cat_fact,
        }

        return JSONResponse(content=data, media_type="application/json", status_code=200)

    except httpx.RequestError as e:
        logger.error(f"Network error fetching cat fact: {e}")
        fallback_data = {
            "status": "success",
            "user": {
                "email": "bamjoe464@gmail.com",
                "name": "Joseph Ayeni",
                "stack": "Python/FastAPI"
            },
            "timestamp": current_time,
            "fact": "Unable to fetch cat fact at the moment",
        }
        return JSONResponse(content=fallback_data, media_type="application/json", status_code=200)

    except Exception as e:
        logger.exception("Unexpected error occurred")
        error_data = {
            "status": "error",
            "message": "Something went wrong on the server",
            "timestamp": current_time,
        }
        return JSONResponse(content=error_data, media_type="application/json", status_code=500)
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
