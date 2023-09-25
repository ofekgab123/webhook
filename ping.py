from fastapi import APIRouter
from fastapi.responses import JSONResponse


pingRoute = APIRouter()

@pingRoute.get('/ping')
def ping(): 

    response = {
        "msg": "pong",
        "status": 200
    }

    return JSONResponse(status_code=200,content=response)