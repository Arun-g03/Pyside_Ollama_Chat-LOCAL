#!/usr/bin/env python3
"""
Simple test to check Ollama connection and model response times
"""

import requests
import json
import time
import subprocess
import platform

def test_ollama_connection():
    """Test Ollama connection and model response"""
    print("=== Ollama Connection Test ===")
    
    # Test 1: Check if Ollama is running
    print("\n1. Checking if Ollama is running...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            print(f"Available models: {models}")
        else:
            print(f"❌ Ollama returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False
    
    # Test 2: Try a simple chat request with timeout
    if models:
        test_model = models[0]  # Use first available model
        print(f"\n2. Testing chat with model: {test_model}")
        
        payload = {
            "model": test_model,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, please respond with just 'Hi there!'"
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        print("Sending test message...")
        start_time = time.time()
        
        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json=payload,
                timeout=60  # 60 second timeout
            )
            
            elapsed_time = time.time() - start_time
            print(f"Response received in {elapsed_time:.2f} seconds")
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('message', {}).get('content', 'No response')
                print(f"✅ Success! AI Response: {ai_response}")
                return True
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"❌ Timeout after {elapsed_time:.2f} seconds")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("❌ No models available")
        return False

def test_ollama_process():
    """Check Ollama process status"""
    print("\n3. Checking Ollama process...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Ollama CLI working")
            print("Installed models:")
            print(result.stdout)
        else:
            print("❌ Ollama CLI error")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Ollama CLI error: {e}")

if __name__ == "__main__":
    success = test_ollama_connection()
    test_ollama_process()
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")