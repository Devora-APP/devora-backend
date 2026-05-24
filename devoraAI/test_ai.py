import httpx
import asyncio

async def test():
    print("Testing /api/v1/inquiry endpoint...")
    payload = {"prompt": "write a Python function to check if a number is prime", "language": "auto"}
    timeout = httpx.Timeout(120.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            r = await client.post("http://localhost:8000/api/v1/inquiry", json=payload)
            print(f"Status Code: {r.status_code}")
            print(f"Response JSON: {r.json()}")
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(test())
