import httpx
import asyncio
import json

system_prompt = """You are DEVORA, an elite AI coding assistant.
You must respond with ONLY a JSON object exactly matching this schema:
{
  "language": "python",
  "code_lines": [
    "def example():",
    "    print('hello world')"
  ],
  "explanation": ["step 1", "step 2"],
  "complexity": "O(n) time, O(1) space"
}
Output pure JSON format.
"""

payload = {
    "model": "deepseek-r1:1.5b",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "write a Python function to check if a number is prime"}
    ],
    "format": "json",
    "stream": False,
    "options": {"temperature": 0.2, "num_predict": 2048}
}

async def test():
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post("http://127.0.0.1:11434/api/chat", json=payload)
        print("RAW OUTPUT:")
        print(r.json()["message"]["content"])

asyncio.run(test())
