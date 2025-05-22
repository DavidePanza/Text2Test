from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import httpx
from typing import List, Optional
import os

app = FastAPI()

# Model name
MODEL_NAME = os.environ.get("MODEL_NAME", "gemma3:4b")
OLLAMA_API = "http://localhost:11434/api"

# Define models
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/generate")
async def generate(request: GenerateRequest):
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": request.prompt,
            "stream": False,
            "options": {
                "num_predict": request.max_tokens
            }
        }
        
        # Print debugging info
        print(f"Sending request to Ollama: {payload}")
        
        # Make the request to Ollama
        response = httpx.post(
            f"{OLLAMA_API}/generate",
            json=payload,
            timeout=120.0
        )
        
        # Get the raw text from the response
        raw_text = response.text
        
        # Print the raw response for debugging
        print(f"Raw response from Ollama: {raw_text[:200]}...")
        
        # Return the raw text as plain text instead of trying to parse it
        return Response(content=f"Raw response: {raw_text}", media_type="text/plain")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return Response(content=f"Error: {str(e)}", media_type="text/plain")