import json
from typing import Annotated
from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn
import requests
from ping import pingRoute
import os
from dotenv import load_dotenv, find_dotenv

app = FastAPI()
app.include_router(pingRoute)

 
env = load_dotenv(find_dotenv())
if env == False:
    logger.warning("Could not find .env file")

MAYTAPI_KEY = os.environ.get("MAYTAPI_KEY")
    
if MAYTAPI_KEY == None:
    logger.error("Could not find MAYTAPI_KEY env var.")
    exit(1)


def sendMsg(phone):
    url = 'https://api.maytapi.com/api/1ece67a7-b614-442e-9fe7-5a7db00ffc09/32888/sendMessage'
    payload = {
        "to_number": phone,
        "type": "text",
        "message": "מה המצב?"
    }
    headers = {
        "Content-Type": "application/json", 
        "x-maytapi-key": MAYTAPI_KEY
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)   
    if response.status_code == 200:
        logger.info('POST Request with JSON payload was successful')
        logger.debug('Response:', response.text)
    else:
        logger.error('POST Request with JSON payload failed with status code:', response.status_code)


@app.post('/webhook')
async def webhook(  request: Request,
                    content_type: Annotated[str | None, Header()] = None):
    
    if content_type != 'application/json':
        
        response = {
            "msg": "Wrong Content-Type header",
            "status": 415
        }
        
        logger.error("Wrong Content-Type header. needs to be => application/json" )
        
        return JSONResponse(status_code=415,content=response)
    
    try:
        payload = await request.json()
        logger.debug("request payload:", payload)
        user = payload.get('user', {})
        phone = user.get('phone')
        
    except :
        response = {
            "msg": "Bad request: Invalid JSON",
            "status": 400
        }
        logger.error(response.get('msg'))
        return JSONResponse(status_code=400,content=response)

    sendMsg(phone)
    
    response = {
        "msg": "Success",
        "payload": phone,
        "status": 200
    }
    return JSONResponse(status_code=200,content=response)

if __name__ == "__main__":
    uvicorn.run( "basicWebhook:app",
                  host='0.0.0.0',
                  port=5000, 
                  log_level="info",
                  reload=True)
