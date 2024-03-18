from llama_index.core import VectorStoreIndex, SummaryIndex, DocumentSummaryIndex, SimpleDirectoryReader
from llama_index.readers.github import GithubRepositoryReader
from llama_index.readers.web import SimpleWebPageReader

from functools import lru_cache
import re
import requests, os

from query_agents.indexer.utils import response_synthesizer, chatgpt, splitter

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
  
from llama_index.core import VectorStoreIndex, SummaryIndex

from llama_index.readers.github import GithubRepositoryReader

class web_agent:
  def __init__(self, url, index_regex:str=r'.+\.(md|txt)$'):
    self.initialized = False
    github_urls = self.fetch_github_repo_contents_urls(url)
    print(f"Extracted {len(github_urls)} in total from repo")
    github_urls = self.filter_urls(
      github_urls, regex=index_regex)
    print(f"Filtered to {len(github_urls)} urls")
    self._init_web_document_index(github_urls)
    
  def _init_web_document_index(self, urls:list, llm=True):
    documents = SimpleWebPageReader(html_to_text=True).load_data(
      urls
    )
    if llm:
      self.doc_index = DocumentSummaryIndex.from_documents(
          documents,
          llm=chatgpt,
          transformations=[splitter],
          response_synthesizer=response_synthesizer,
          # show_progress=True,
      )
    else:
      self.doc_index = SummaryIndex.from_documents(documents)
    self._init_query_engine(self.doc_index)
  
  def _init_query_engine(self, index):
    self.query_engine = index.as_query_engine(streaming=True)
    self.initialized = True
  
  def query(self, query):
    return self.query_engine.query(query)
  
  def filter_urls(
    self, urls, regex:str=None, limit:int=None):
    if regex: 
      pattern = re.compile(regex, re.IGNORECASE)
      urls=[
        l for l in urls if pattern.search(l)]
    if limit: urls=urls[:min(len(urls), limit)]
    return urls
    
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
            # print(f"Filename:{content.get('name','')}")
            # If it's a directory, recurse into it
            if content.get('type') == 'dir':
                urls.extend(self.fetch_github_repo_contents_urls(api_url+path, content.get('path')))
            else:
                # Append the file URL to the list
                urls.append(content.get('html_url', 'No URL found'))
        print(f"Extracted: {n} urls here")
    # else:
    #     # Print out the error message from GitHub API
    #     print(f"Error fetching contents: {response.status_code} - {response.json().get('message')}")
    return urls
  
  @property
  def _documents(self):
    if hasattr(self, 'documents'):
      return self.documents

class directory_agent(web_agent):
  def __init__(self, local_path, exts_filter:list=[".md", ".txt", ".yaml", ".json"]):
    self._init_web_document_index(local_path, exts_filter)
  
  def _init_web_document_index(
    self, path, exts_filter, llm=True, model="gpt-4"):
    self.documents = SimpleDirectoryReader(
      path, recursive=True, required_exts=exts_filter
    ).load_data()
    if llm:
      # splitter = SentenceSplitter(chunk_size=1024)
      self.doc_index = DocumentSummaryIndex.from_documents(
        self.documents,
        llm=chatgpt,
        transformations=[splitter],
        response_synthesizer=response_synthesizer,
        # show_progress=True,
      )
    else:
      self.doc_index = SummaryIndex.from_documents(self.documents)
    self._init_query_engine(self.doc_index)
    
if __name__=="__main__":
  web_agent