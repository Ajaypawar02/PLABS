import os
import sys
import yaml
import requests
sys.path.append("./")
sys.path.append("./app")
repo_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(repo_dir)
import pybrake
import json
import time
import uvicorn
from schemas import *
from pybrake.middleware.fastapi import init_app
from src import logging
from retry import retry
from mangum import Mangum
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.pipeline.summarization import Summarization
from langchain.llms import OpenAIChat
from src.pipeline.generation import generate_article_without_internet, generate_article_with_internet, article_type_mapping
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv
from threading import Thread
load_dotenv()
logger = logging.getLogger(__name__)
MODEL_THRESHOLD = os.getenv("MODEL_THRESHOLD")

app = FastAPI(debug=True)


@app.get("/")
def read_root():
    return {"response": "Service is ready to run"}


@app.post("/generate_summary")
def generate_summary(request: Request, payload: SUMMARYPARAMETERS):
    try:
        api_params = json.loads(payload.json())
        summary = Summarization(api_params["model"]).summarize(api_params["text"])

        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}
    


@app.post('/generate_article')
async def generate_article(request: Request, payload: GENERATIONPARAMETERS):
    data = json.loads(payload.json())
    
    use_internet = data.get('use_internet', False)
    model_id = data.get('model_id', 'gpt-4')



    # Initialize LLM
    if model_id == "gpt-4":
        llm = OpenAIChat(temperature=0.9, model_name= data["model_id"], streaming=True,  callbacks = [StreamingStdOutCallbackHandler()])

    else:
        llm = OpenAIChat(temperature=0.9, model_name= data["model_id"], streaming=True,  callbacks = [StreamingStdOutCallbackHandler()])


    
    if use_internet == False:
        result = generate_article_without_internet(data, llm)
    else:
        result = generate_article_with_internet(data, llm)



    return result


handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT_NO")))
    print("Setup Complete")

# air_brake_logger = airbrake.getLogger(api_key = os.getenv("AIRBRAKE_KEY"), project_id = os.getenv("AIRBRAKE_ID"), environment = os.getenv("AIRBRAKE_ENV"))
