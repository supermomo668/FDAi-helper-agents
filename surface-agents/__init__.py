%env OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
from llama_index.core import VectorStoreIndex
from llama_index.readers.github import GithubRepositoryReader
from IPython.display import Markdown, display
import os