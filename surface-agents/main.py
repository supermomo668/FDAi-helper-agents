from fastapi import FastAPI
from app.routers import github_assistant

from dotenv import load_dotenv

app = FastAPI()
# Apply nest_asyncio to enable nested event loops
nest_asyncio.apply()

app = FastAPI()

# Initialize global variables
load_dotenv()  
# take environment variables from .env.

query_engine = None

app.include_router(github_assistant.router)
