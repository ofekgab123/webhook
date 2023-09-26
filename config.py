import os
import sys
from dotenv import load_dotenv, find_dotenv
from loguru import logger

def __init_Settings() -> dict:
    config = {}
    env = load_dotenv(find_dotenv())
    if env == False:
        logger.warning("Could not find .env file")

    MAYTAPI_KEY = os.environ.get("MAYTAPI_KEY")
    if MAYTAPI_KEY == None:
        logger.error("Could not find MAYTAPI_KEY env var.")
        sys.exit(1)
    else:
        config.update({"MAYTAPI_KEY":MAYTAPI_KEY})
        
    MAYTAPI_URL = os.environ.get("MAYTAPI_URL")
    if MAYTAPI_URL == None:
        logger.error("Could not find MAYTAPI_URL env var.")
        sys.exit(1)
    else:
        config.update({"MAYTAPI_URL":MAYTAPI_URL})
            
    return config

settings=__init_Settings()