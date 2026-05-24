import httpx
import logging

async def call_ollama(system_prompt: str, user_message: str) -> str:
    """
    Makes an async POST request to local Ollama API chat completions.
    We target deepseek-coder by default and return the raw Markdown string.
    """
    url = "http://127.0.0.1:11434/api/chat"
    
    payload = {
        "model": "deepseek-r1:1.5b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 2048
        }
    }

    timeout = httpx.Timeout(120.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code != 200:
                raise Exception(f"Ollama API Error: {response.status_code} - {response.text}")
            
            data = response.json()
            return data["message"]["content"]
                
    except httpx.ConnectError:
        logging.warning("Ollama is not running. Returning mock response.")
        
        if "debug" in user_message.lower():
            return "```python\ndef mock_fixed_code():\n    print('fixed')\n```\n\nMOCK: Added missing print formatting."
        else:
            return "```python\ndef is_prime(n):\n    if n <= 1: return False\n    return True\n```\n\nMOCK: We simply check if the value is less than 1."
            
    except httpx.TimeoutException:
        raise Exception("Request to Ollama API timed out. Try loading a smaller model or giving it more time.")
