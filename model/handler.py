import runpod
import requests
import time


def handler(event):
    try:
        job_input = event.get("input", {})
        
        # Chat format - multi-turn conversation
        if "messages" in job_input:
            return handle_chat(job_input)
        
        # Generate format - single completion
        elif "prompt" in job_input:
            return handle_generate(job_input)
        
        else:
            return {
                "success": False,
                "error": "Must provide either 'messages' (for chat) or 'prompt' (for generate)"
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_chat(job_input):
    """Handle conversational chat with message history"""
    payload = {
        "model": "gemma3:12b-it-qat",
        "messages": job_input["messages"],
        "stream": False,
        "options": {
            "temperature": job_input.get("temperature", 0.7),
            "top_p": job_input.get("top_p", 0.9),
            "num_predict": job_input.get("max_tokens", 256)
        }
    }
    
    response = requests.post('http://localhost:11434/api/chat', json=payload, timeout=120)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "success": True,
            "response": data.get("response", ""),
            "type": "chat",
            "message_count": len(job_input["messages"])
        }
    else:
        return {"success": False, "error": f"Chat API error: {response.status_code}"}

def handle_generate(job_input):
    """Handle single-turn text generation"""
    payload = {
        "model": "gemma3:12b-it-qat",
        "prompt": job_input["prompt"],
        "stream": False,
        "options": {
            "temperature": job_input.get("temperature", 0.7),
            "top_p": job_input.get("top_p", 0.9),
            "num_predict": job_input.get("max_tokens", 256)
        }
    }
    
    # Add system prompt if provided
    if job_input.get("system"):
        payload["system"] = job_input["system"]
    
    response = requests.post('http://localhost:11434/api/generate', json=payload, timeout=120)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "success": True,
            "response": data.get("response", ""),
            "type": "generate",
            "prompt_length": len(job_input["prompt"])
        }
    else:
        return {"success": False, "error": f"Generate API error: {response.status_code}"}

# This is the correct way to start RunPod serverless
if __name__ == "__main__":
    print("Starting RunPod serverless handler...")
    runpod.serverless.start({"handler": handler})
