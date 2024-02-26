from fastapi import FastAPI
from routers import github_assistant

from dotenv import load_dotenv

app = FastAPI(lifespan=github_assistant.load_agent)
# Apply nest_asyncio to enable nested event loops
# nest_asyncio.apply()

# Initialize global variables
load_dotenv()  
# take environment variables from .env.

query_engine = None

app.include_router(github_assistant.router)
