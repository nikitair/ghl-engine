import os
import time
import json

import aiofiles
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, Response

from config import HOST, PORT, ROOT_DIR
from config.logging_config import logger

load_dotenv()

app = FastAPI()

@app.get("/", include_in_schema=False, name="Index")
async def index():
    return {"service": "GHL Engine"}


@app.get("/health-check", include_in_schema=True, name="Health Check")
async def health_check(request: Request) -> dict:
    return Response(
        content=json.dumps(
            {   
                "service": "GHL Engine",
                "action": "Health Check",
                "headers": dict(request.headers),
                "host": request.client.host,
                "port": request.client.port,
                "user-agent": request.headers.get("User-Agent"),
                "path": request.url.path,
                "query_string": request.url.query,
                "scheme": request.url.scheme,
                "hostname": request.url.hostname,
                "cookies": request.cookies,
                "method": request.method,
                "http_version": request.scope['http_version'],
                "root_path": request.scope['root_path']
            }
        ),
        status_code=202,
        media_type="application/json"
    )


@app.get("/logs", include_in_schema=False, name="Logs")
async def show_logs() -> PlainTextResponse:
    logger.info(f"*** API Get Logs")
    try:
        logs_path = os.path.join(ROOT_DIR, "logs", "logs.log")
        with aiofiles.open(logs_path, "r") as lf:
            file_lines: list = await lf.readlines()
            file_lines.reverse()
            file = ''.join(file_lines)
            return PlainTextResponse(content=file)
    except FileNotFoundError or FileExistsError as ex:
        logger.error(f"!!! FILE FINDING ERROR - ({ex})")
        raise HTTPException(
            status_code=404,
            detail={"error": f"File reading error: ({ex})"}
        )
    except Exception as ex:
        logger.exception(f"!!!! FILE READING UNEXPECTED ERROR - ({ex})")
        raise HTTPException(
            status_code=500,
            detail={"error": f"Unexpected error: ({ex})"}
        )


if __name__ == "__main__":
    # set system time to UTC
    os.environ['TZ'] = 'UTC'
    time.tzset()
    
    uvicorn.run(app=app, host=HOST, port=PORT)