from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from typing import List, Optional, Dict, Any
import os
import json

app = FastAPI()

# Model name
MODEL_NAME = os.environ.get("MODEL_NAME", "gemma3:4b")
OLLAMA_API = "http://localhost:11434/api"

# Define models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2048
    top_p: Optional[float] = 0.9

class GenerateRequest(BaseModel):
    prompt: str
    system: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2048
    top_p: Optional[float] = 0.9

@app.get("/health")
async def health():
    try:
        response = httpx.get(f"{OLLAMA_API}/tags")
        return {"status": "healthy" if response.status_code == 200 else "unhealthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "top_p": request.top_p,
                "num_predict": request.max_tokens
            }
        }
        
        response = httpx.post(
            f"{OLLAMA_API}/chat",
            json=payload,
            timeout=120.0
        )
        response.raise_for_status()
        
        # Extract just the response field from Ollama's response
        try:
            data = json.loads(response.text)
            return {
                "response": data.get("response", ""),
                "model": data.get("model", ""),
                "done": data.get("done", False)
            }
        except json.JSONDecodeError:
            # If we can't parse as JSON, return the raw text
            return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate(request: GenerateRequest):
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": request.prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "top_p": request.top_p,
                "num_predict": request.max_tokens
            }
        }
        
        if request.system:
            payload["system"] = request.system
            
        response = httpx.post(
            f"{OLLAMA_API}/generate",
            json=payload,
            timeout=120.0
        )
        response.raise_for_status()
        
        # Extract just the response field from Ollama's response
        try:
            data = json.loads(response.text)
            return {
                "response": data.get("response", ""),
                "model": data.get("model", ""),
                "done": data.get("done", False)
            }
        except json.JSONDecodeError:
            # If we can't parse as JSON, return the raw text
            return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))