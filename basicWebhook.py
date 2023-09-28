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
MAYTAPI_URL = settings.get("MAYTAPI_URL")
MAYTAPI_KEY = settings.get("MAYTAPI_KEY")


def StartSession(phone):
    openmsg = "שלום זאת העוזרת הטכנלוגית של מיכל כהן אשמח לעזור לך במה שתצטרכי"
    buttons = [
        {
            "id": "AnswerOpenMsg1",
            "text": "לעולם הלייזר",
        },
        {
            "id": "AnswerOpenMsg2",
            "text": "לעולמות הקוסמטיקה",
        },
        {
            "id": "AnswerOpenMsg3",
            "text": "למוצרים שלנו",
        },
        {
            "id": "AnswerOpenMsg4",
            "text": "אם לא הצלחתי לעזור לך ואת מעוניינת לדבר עם מיכל ",
        },
    ]
    payload = {
        "to_number": phone,
        "type": "buttons",
        "message": openmsg,
        "buttons": buttons,
    }
    headers = {
        "Content-Type": "application/json",
        "x-maytapi-key": MAYTAPI_KEY,
    }
    try:
        response = requests.post(
            MAYTAPI_URL, data=json.dumps(payload), headers=headers, timeout=200
        )
        if response.status_code == 200:
            logger.info("POST Request with JSON payload was successful")
            logger.debug("Response:", response)
        else:
            logger.error(
                "POST Request with JSON payload failed with status code:",
                response.status_code,
            )
            logger.debug("Response:", response)

    except requests.Timeout:
        logger.error("POST Request timeout after 200 seconds")
        return JSONResponse(
            status_code=408, content="POST Request timeout after 200 seconds"
        )
    except requests.ConnectionError:
        logger.error("POST Request connection error")
        return JSONResponse(status_code=503, content="POST Request connection error")


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

    StartSession(phone)

    logger.debug("payload phone: ", phone)

    response = {"msg": "Success", "status": 200}
    return JSONResponse(status_code=200, content=response)


if __name__ == "__main__":
    uvicorn.run("basicWebhook:app", host="0.0.0.0", port=5000, log_level="debug")
