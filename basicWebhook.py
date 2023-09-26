import json
from typing import Annotated
from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn
import requests

from ping import pingRoute
from config import settings


app = FastAPI()
app.include_router(pingRoute)


def sendMsg(phone):
    url = settings.get("MAYTAPI_URL")
    payload = {"to_number": phone, "type": "text", "message": "מה המצב?"}
    headers = {
        "Content-Type": "application/json",
        "x-maytapi-key": settings.get("MAYTAPI_KEY"),
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=20)
    if response.status_code == 200:
        logger.info("POST Request with JSON payload was successful")
        logger.debug("Response:", response.text)
    else:
        logger.error(
            "POST Request with JSON payload failed with status code:",
            response.status_code,
        )


@app.post("/webhook")
async def webhook(
    request: Request, content_type: Annotated[str | None, Header()] = None
):
    if content_type != "application/json":
        response = {"msg": "Wrong Content-Type header", "status": 415}

        logger.error("Wrong Content-Type header. needs to be => application/json")

        return JSONResponse(status_code=415, content=response)

    try:
        payload = await request.json()
        logger.debug("request payload:", payload)
        user = payload.get("user", {})
        phone = user.get("phone")

    except:
        response = {"msg": "Bad request: Invalid JSON", "status": 400}
        logger.error(response.get("msg"))
        return JSONResponse(status_code=400, content=response)

    # sendMsg(phone)

    response = {"msg": "Success", "payload": phone, "status": 200}
    return JSONResponse(status_code=200, content=response)


if __name__ == "__main__":
    uvicorn.run(
        "basicWebhook:app", host="0.0.0.0", port=5000, log_level="info", reload=True
    )
