# import runpod
# import httpx
# import time
# import sys

# # Add parent directory to path so we can import from src
# sys.path.append('/app')

# # FastAPI URL
# API_URL = "http://localhost:8000"

# def handler(event):
#     """
#     RunPod handler function with FastAPI
#     """
#     try:
#         job_input = event.get("input", {})
        
#         # Determine which endpoint to use based on input
#         if "messages" in job_input:
#             endpoint = "/chat"
#         elif "prompt" in job_input:
#             endpoint = "/generate"
#         else:
#             return {"error": "Invalid input: must contain either 'messages' or 'prompt'"}
        
#         # Make request to FastAPI
#         response = httpx.post(
#             f"{API_URL}{endpoint}",
#             json=job_input,
#             timeout=120.0
#         )
        
#         if response.status_code == 200:
#             return {"output": response.json()}
#         else:
#             return {
#                 "error": f"API Error: {response.status_code}",
#                 "details": response.text
#             }
            
#     except Exception as e:
#         return {"error": f"Unexpected error: {str(e)}"}

# # Start runpod handler
# if __name__ == "__main__":
#     # Start RunPod serverless
#     runpod.serverless.start({"handler": handler})

# new version 

import requests
import subprocess
import json
import time
import os
import model

def check_system_status():
    """Check if all services are running properly"""
    status = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ollama_process": False,
        "ollama_api": False,
        "model_available": False,
        "port_11434": False,
        "errors": []
    }
    
    try:
        # Check if Ollama process is running
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'ollama' in result.stdout:
            status["ollama_process"] = True
        else:
            status["errors"].append("Ollama process not found")
    except Exception as e:
        status["errors"].append(f"Process check failed: {str(e)}")
    
    try:
        # Check if port 11434 is listening
        result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True)
        if '11434' in result.stdout:
            status["port_11434"] = True
        else:
            status["errors"].append("Port 11434 not listening")
    except Exception as e:
        status["errors"].append(f"Port check failed: {str(e)}")
    
    try:
        # Check Ollama API
        response = requests.get('http://localhost:11434/api/tags', timeout=10)
        if response.status_code == 200:
            status["ollama_api"] = True
            models_data = response.json()
            model_names = [model['name'] for model in models_data.get('models', [])]
            status["available_models"] = model_names
            
            # Check for specific model
            if 'gemma3:12b-it-qat' in model_names:
                status["model_available"] = True
            else:
                status["errors"].append(f"gemma3:12b-it-qat not found. Available: {model_names}")
        else:
            status["errors"].append(f"Ollama API returned {response.status_code}: {response.text}")
    except Exception as e:
        status["errors"].append(f"Ollama API check failed: {str(e)}")
    
    return status

def test_model_generation(prompt="Hello, respond with just 'OK'", timeout=60):
    """Test if the model can actually generate text"""
    try:
        start_time = time.time()
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "gemma3:12b-it-qat",
                "prompt": prompt,
                "stream": False
            },
            timeout=timeout
        )
        
        generation_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "response": result.get('response', 'No response field'),
                "model": result.get('model', 'Unknown model'),
                "generation_time_seconds": round(generation_time, 2),
                "prompt_length": len(prompt)
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "generation_time_seconds": round(generation_time, 2)
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "generation_time_seconds": round(time.time() - start_time, 2) if 'start_time' in locals() else 0
        }

def handler(job):
    """Main handler with comprehensive logging"""
    start_time = time.time()
    
    # Log the incoming job
    job_info = {
        "job_received": True,
        "job_keys": list(job.keys()) if isinstance(job, dict) else "Not a dict",
        "input_data": job.get('input', {}) if isinstance(job, dict) else str(job)[:200]
    }
    
    # Check system status first
    print("🔍 Checking system status...")
    system_status = check_system_status()
    
    # If Ollama isn't ready, try to wait and retry
    if not system_status["ollama_api"] or not system_status["model_available"]:
        print("⏳ Ollama not ready, waiting 15 seconds...")
        time.sleep(15)
        system_status = check_system_status()
    
    # If still not ready, one more try with longer wait
    if not system_status["ollama_api"]:
        print("⏳ Still not ready, waiting another 30 seconds...")
        time.sleep(30)
        system_status = check_system_status()
    
    # Test model generation with simple prompt first
    print("🧪 Testing model generation...")
    generation_test = test_model_generation()
    
    # Prepare comprehensive response
    diagnostic_info = {
        "job_info": job_info,
        "system_status": system_status,
        "generation_test": generation_test,
        "container_info": {
            "hostname": os.environ.get('HOSTNAME', 'unknown'),
            "pwd": os.getcwd(),
            "python_version": subprocess.run(['python3', '--version'], capture_output=True, text=True).stdout.strip(),
            "total_handler_time": 0  # Will be filled at the end
        }
    }
    
    # If everything looks good, try the actual generation
    if system_status["model_available"] and generation_test["success"]:
        try:
            # Get the actual prompt from the job
            if isinstance(job, dict) and 'input' in job:
                prompt = job['input'].get('prompt', 'Hello, how are you?')
            else:
                prompt = 'Hello, how are you?'
            
            print(f"🚀 Generating response for prompt: {prompt[:50]}...")
            
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    "model": "gemma3:12b-it-qat",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120  # 2 minutes timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                total_time = time.time() - start_time
                diagnostic_info["container_info"]["total_handler_time"] = round(total_time, 2)
                
                return {
                    "success": True,
                    "response": result.get('response', 'No response field found'),
                    "model_used": result.get('model', 'Unknown'),
                    "prompt_used": prompt,
                    "diagnostics": diagnostic_info
                }
            else:
                total_time = time.time() - start_time
                diagnostic_info["container_info"]["total_handler_time"] = round(total_time, 2)
                
                return {
                    "success": False,
                    "error": f"Generation failed: HTTP {response.status_code}",
                    "response_text": response.text,
                    "diagnostics": diagnostic_info
                }
                
        except Exception as e:
            total_time = time.time() - start_time
            diagnostic_info["container_info"]["total_handler_time"] = round(total_time, 2)
            
            return {
                "success": False,
                "error": f"Generation exception: {str(e)}",
                "diagnostics": diagnostic_info
            }
    
    # If we get here, something is wrong with the setup
    total_time = time.time() - start_time
    diagnostic_info["container_info"]["total_handler_time"] = round(total_time, 2)
    
    return {
        "success": False,
        "error": "System not ready for generation",
        "diagnostics": diagnostic_info
    }

# RunPod serverless handler
model.serverless.start({"handler": handler})

# For local testing
if __name__ == "__main__":
    test_job = {"input": {"prompt": "Test prompt"}}
    result = handler(test_job)
    print(json.dumps(result, indent=2))