#!/usr/bin/env python3
"""
Test script to check if Ollama is running on localhost port 11434.
Sends a GET request to http://127.0.0.1:11434 and asserts the response is 'Ollama is running'.
"""

import json
import sys

# Try to import requests, fall back to urllib if not available
try:
    import requests
    USE_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    USE_REQUESTS = False


def make_request(url, method='GET', data=None):
    """
    Make an HTTP request using requests or urllib.
    Returns (success: bool, response_data: dict or str, error_message: str)
    """
    if USE_REQUESTS:
        try:
            if method == 'GET':
                response = requests.get(url, timeout=10)
            elif method == 'POST':
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            return True, response.json() if 'json' in response.headers.get('content-type', '') else response.text, ""
        except requests.exceptions.RequestException as e:
            return False, None, str(e)
        except Exception as e:
            return False, None, str(e)
    else:
        try:
            if method == 'POST' and data:
                data = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            else:
                req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8')
                try:
                    return True, json.loads(content), ""
                except json.JSONDecodeError:
                    return True, content, ""
        except urllib.error.URLError as e:
            return False, None, str(e)
        except Exception as e:
            return False, None, str(e)

def test_ollama_connection():
    url = "http://127.0.0.1:11434"
    print(f"Testing Ollama connection at {url}...")
    success, data, error = make_request(url)
    assert success and data == "Ollama is running", f"Expected 'Ollama is running', got {data}"
    print("Ollama is running!")

if __name__ == "__main__":
    test_ollama_connection()