import runpod
import httpx
import time
import sys

# Add parent directory to path so we can import from src
sys.path.append('/app')

# FastAPI URL
API_URL = "http://localhost:8000"

def handler(event):
    """
    RunPod handler function with FastAPI
    """
    try:
        job_input = event.get("input", {})
        
        # Determine which endpoint to use based on input
        if "messages" in job_input:
            endpoint = "/chat"
        elif "prompt" in job_input:
            endpoint = "/generate"
        else:
            return {"error": "Invalid input: must contain either 'messages' or 'prompt'"}
        
        # Make request to FastAPI
        response = httpx.post(
            f"{API_URL}{endpoint}",
            json=job_input,
            timeout=120.0
        )
        
        if response.status_code == 200:
            return {"output": response.json()}
        else:
            return {
                "error": f"API Error: {response.status_code}",
                "details": response.text
            }
            
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# Start runpod handler
if __name__ == "__main__":
    # Start RunPod serverless
    runpod.serverless.start({"handler": handler})


