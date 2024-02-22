from fastapi import APIRouter, HTTPException
from llama_index.core import VectorStoreIndex
from llama_index.readers.github import GithubRepositoryReader
import os

from dependencies import _REQUIRED_ENV_VARS

router = APIRouter()

@router.on_event("startup")
async def load_index():
    global query_engine
    documents = GithubRepositoryReader(
        github_token=os.getenv("GITHUB_TOKEN"),
        owner=os.getenv("GITHUB_REPO_OWNER"),
        repo=os.getenv("GITHUB_REPO_NAME"),
        use_parser=False,
        verbose=False,
        ignore_directories=["examples"],
    ).load_data(branch=os.getenv("GITHUB_REPO_BRANCH", "main"))
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

@router.get("/query/")
async def query_llama_index(query: str):
    if 'query_engine' not in globals():
        raise HTTPException(status_code=503, service_unavailable="Index not loaded")
    response = query_engine.query(query, verbose=True)
    return response
