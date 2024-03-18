
from llama_index.core import  get_response_synthesizer
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter

response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", use_async=False
)

splitter = SentenceSplitter(chunk_size=1024)

chatgpt = OpenAI(temperature=0, model="gpt-3.5-turbo")