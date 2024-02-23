from fastapi import APIRouter, HTTPException
from .github_index import github_agent, web_agent
import os

router = APIRouter()

@router.on_event("startup")
async def load_index():
    global query_agent
    query_agent = web_agent()
    # query_agent = github_agent()
    
@router.get("/query/")
async def query_llama_index(query: str):
    if 'query_agent' not in globals():
        raise HTTPException(status_code=503, service_unavailable="Index not loaded")
    return query_agent.make_github_query(query)

if __name__=="__main__":
    from dotenv import load_dotenv
    load_dotenv('.env')
    query_agent = web_agent()
    PROMPT= "What is the GitHub Repository FDAi about?"
    ANS=query_agent.query(PROMPT)
    print(f"Question:{PROMPT}","ANSWER:{ANS}",sep='\n')