import os
from dotenv import load_dotenv, find_dotenv
from loguru import logger

def __Init_settings() -> dict:
  settings = {}
  env = load_dotenv(find_dotenv())
  if env == False:
      logger.warning("Could not find .env file")

  MAYTAPI_KEY = os.environ.get("MAYTAPI_KEY")
  if MAYTAPI_KEY == None:
      logger.error("Could not find MAYTAPI_KEY env var.")
      exit(1)
  else:
     settings.update({"MAYTAPI_KEY":MAYTAPI_KEY})
      
  MAYTAPI_URL = os.environ.get("MAYTAPI_URL")
  if MAYTAPI_URL == None:
      logger.error("Could not find MAYTAPI_URL env var.")
      exit(1)
  else:
     settings.update({"MAYTAPI_URL":MAYTAPI_URL})
     print("load vars")
         
  return settings

settings=__Init_settings()