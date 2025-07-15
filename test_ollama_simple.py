#!/usr/bin/env python3
"""
Simple test script to communicate with Ollama using qwen3:0.6b model
Outputs raw response to terminal without any analysis
"""

import requests
import json

def test_ollama_simple():
    """Test Ollama with qwen3:0.6b model - simple non-streaming request"""
    
    # Ollama API endpoint
    base_url = "http://localhost:11434"
    
    # Test message
    test_message = "hello"
    
    print(f"Testing Ollama with qwen3:0.6b model")
    print(f"Message: {test_message}")
    print("-" * 50)
    
    # Prepare the request
    data = {
        "model": "qwen3:0.6b",
        "messages": [
            {"role": "user", "content": test_message}
        ],
        "stream": False,  # No streaming
        "temperature": 0.7
    }
    
    try:
        # Make the request
        print("Sending request to Ollama...")
        response = requests.post(
            f"{base_url}/api/chat",
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        # Parse the response
        try:
            data = response.json()
            content = data.get("message", {}).get("content", "")
            
            print("Raw response from Ollama:")
            print("-" * 30)
            print(content)
            print("-" * 50)
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Ollama. Make sure it's running on localhost:11434")
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ollama_simple() 