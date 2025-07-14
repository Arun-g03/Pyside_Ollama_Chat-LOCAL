import platform
import subprocess
import time
import requests
import json

def is_ollama_running():
    """Check if Ollama is running and accessible"""
    try:
        # Try to connect to Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False

def is_ollama_installed():
    """Check if Ollama is installed and accessible"""
    try:
        result = subprocess.run(
            ["ollama", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return False

def get_available_models():
    """Get list of available models from Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            return models
        else:
            print(f"Error fetching models: HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"Error getting models: {e}")
        return []

def send_test_message(model_name, message="Hello, this is a test message. Please respond with a simple greeting."):
    """Send a test message to Ollama and get response"""
    try:
        print(f"Sending test message to model: {model_name}")
        
        # Prepare the request payload
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        # Send the request
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get('message', {}).get('content', 'No response content')
            print(f"AI Response: {ai_response}")
            return True, ai_response
        else:
            print(f"Error sending message: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"Error sending test message: {e}")
        return False, None

def start_ollama_app_windows():
    """Start Ollama on Windows"""
    try:
        print("Starting Ollama on Windows...")
        
        # Start Ollama process
        process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print(f"Ollama process started with PID: {process.pid}")
        return True
        
    except Exception as e:
        print(f"Error starting Ollama on Windows: {e}")
        return False

def start_ollama_app_mac():
    """Start Ollama on macOS"""
    try:
        print("Starting Ollama on macOS...")
        
        # Start Ollama process
        process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print(f"Ollama process started with PID: {process.pid}")
        return True
        
    except Exception as e:
        print(f"Error starting Ollama on macOS: {e}")
        return False

def preflight_check_ollama_app():
    if is_ollama_running():
        print("Ollama server is already running.")
        return True

    print("Ollama server not running. Attempting to start the app...")

    if platform.system() == "Windows":
        success = start_ollama_app_windows()
    elif platform.system() == "Darwin":
        success = start_ollama_app_mac()
    else:
        print("Unsupported OS for automatic Ollama app launch.")
        return False

    if not success:
        return False

    # Wait for server to come up
    for _ in range(15):
        if is_ollama_running():
            print("Ollama is now running.")
            return True
        time.sleep(1)

    print("Ollama app launched but server not responding.")
    return False

def test_ollama_connection():
    """Test the complete Ollama connection and startup process"""
    print("=== Ollama Autostart Test ===")
    print(f"Platform: {platform.system()}")
    print(f"Ollama installed: {is_ollama_installed()}")
    print(f"Ollama running: {is_ollama_running()}")
    
    if not is_ollama_installed():
        print("ERROR: Ollama is not installed. Please install Ollama first.")
        print("Download from: https://ollama.com/download")
        return False
    
    if not is_ollama_running():
        print("Attempting to start Ollama...")
        success = preflight_check_ollama_app()
        
        if not success:
            print("FAILED: Could not start Ollama or it's not responding.")
            print("Please start Ollama manually by running 'ollama serve' in a terminal.")
            return False
    else:
        print("SUCCESS: Ollama is already running and accessible.")
    
    # Test model querying
    print("\n=== Testing Model Query ===")
    models = get_available_models()
    if models:
        print(f"SUCCESS: Found {len(models)} available models:")
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
    else:
        print("WARNING: No models found. You may need to pull a model first.")
        print("Try running: ollama pull llama2")
        return True  # Still return True as Ollama is running
    
    # Test sending a message if models are available
    if models:
        print("\n=== Testing Message Sending ===")
        # Try the first available model
        test_model = models[0]
        print(f"Testing with model: {test_model}")
        
        success, response = send_test_message(test_model)
        if success:
            print("SUCCESS: Message sent and response received successfully!")
        else:
            print("FAILED: Could not send message or get response.")
            return False
    else:
        print("\nSKIPPING: Message test (no models available)")
    
    print("\n=== Test Summary ===")
    print("✅ Ollama is running and accessible")
    print(f"✅ Found {len(models)} available models" if models else "⚠️  No models available")
    if models:
        print("✅ Successfully sent test message and received response")
    
    return True

if __name__ == "__main__":
    test_ollama_connection()
