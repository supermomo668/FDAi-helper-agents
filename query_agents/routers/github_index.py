from fastapi import APIRouter, HTTPException
from llama_index.core import VectorStoreIndex, SummaryIndex

from llama_index.readers.github import GithubRepositoryReader
from llama_index.readers.web import SimpleWebPageReader

from functools import lru_cache
import requests
import os

class github_agent:
  def __init__(self):
    self.document_store = self._init_github_document()
    self.query_engine = self._init_query_engine()

  def query(query):
    response = self.query_engine.query(query, verbose=True)
    return response
  
  def _init_query_engine(self):
    index = VectorStoreIndex.from_documents(self.documents_store)
    query_engine = index.as_query_engine()
    return query_engine
      
  def _init_github_document(self):
    documents = GithubRepositoryReader(
        github_token=os.getenv("GITHUB_TOKEN"),
        owner=os.getenv("GITHUB_REPO_OWNER"),
        repo=os.getenv("GITHUB_REPO_NAME"),
        use_parser=False, verbose=False,
        ignore_directories=["examples"],
    ).load_data(branch=os.getenv("GITHUB_REPO_BRANCH", "main"))
    return documents
  
class web_agent:
  def __init__(self, url):
    self.initialized = False
    github_urls = self.fetch_github_repo_contents_urls(url)
    print(f"Extracted {len(github_urls)} in total from repo")
    self.document_store = self._init_document_store(github_urls)
    self.query_engine = self._init_query_engine(self.document_store)
    
  def _init_document_store(self, urls:list):
    documents = SimpleWebPageReader(html_to_text=True).load_data(
      urls
    )
    return documents
  
  def _init_query_engine(self, document_store):
    index = SummaryIndex.from_documents(document_store)
    query_engine = index.as_query_engine()
    return query_engine
  
  def query(self, query):
    return self.query_engine.query(query)
      
  def fetch_github_repo_contents_urls(
    self, api_url,path=""):
    headers = {
        "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(
        api_url+path, headers=headers
    )
    urls = []
        # Check if the request was successful
    if response.status_code == 200:
        contents = response.json()
        # Ensure contents is a list before iterating
        if not isinstance(contents, list):
            return urls

        for n, content in enumerate(contents):
            print(f"Filename:{content.get('name','')}")
            # If it's a directory, recurse into it
            if content.get('type') == 'dir':
                urls.extend(self.fetch_github_repo_contents_urls(api_url+path, content.get('path')))
            else:
                # Append the file URL to the list
                urls.append(content.get('html_url', 'No URL found'))
        print(f"Extracted: {n} urls here")
    else:
        # Print out the error message from GitHub API
        print(f"Error fetching contents: {response.status_code} - {response.json().get('message')}")
    return urls