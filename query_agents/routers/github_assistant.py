from fastapi import APIRouter, HTTPException
from contextlib import asynccontextmanager

from query_agents.github_index import github_agent, web_agent
import os

from ..dependencies import GITHUB_API_URL

router = APIRouter()

GITHUB_API_URL_FORMATTED=GITHUB_API_URL.format(**{
    "owner": os.environ["GITHUB_REPO_OWNER"],
    "repo": os.environ["GITHUB_REPO_NAME"],
})

# @router.on_event("startup")
@asynccontextmanager
async def load_agent():
    global query_agent
    print(f"API of target repo :{GITHUB_API_URL_FORMATTED}")
    query_agent = web_agent(GITHUB_API_URL_FORMATTED)
    # query_agent = github_agent()

@router.get("/")
async def hello_app(hi:str):
    return f"hello {__name__}!"
    
    
@router.get("/query/")
async def query_llama_index(query: str):
    if 'query_agent' not in globals():
        raise HTTPException(status_code=503, service_unavailable="Index not loaded")
    return query_agent.query(query)

if __name__=="__main__":
    from dotenv import load_dotenv
    load_dotenv('.env')
    print(f"Git URL:{GITHUB_API_URL_FORMATTED}")
    query_agent = web_agent(GITHUB_API_URL_FORMATTED)
    PROMPT= "What is the GitHub Repository FDAi about?"
    ANS=query_agent.query(PROMPT)
    print(f"Question:{PROMPT}",f"ANSWER:{ANS}",sep='\n')