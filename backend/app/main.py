import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional
import uvicorn
from .scraper import get_website_data
from .llm_service import llm_service

app = FastAPI(title="Website Cloning Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebsiteURL(BaseModel):
    url: HttpUrl

class CloneResponse(BaseModel):
    html: str
    message: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Website Cloning Service API"}

@app.post("/clone", response_model=CloneResponse)
async def clone_website(website: WebsiteURL):
    try:
        # Step 1: Scrape the website
        website_data = get_website_data(str(website.url))
        
        # Step 2: Generate the clone using LLM
        cloned_html = await llm_service.generate_website_clone(website_data)
        
        return CloneResponse(
            html=cloned_html,
            message="Website cloned successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
