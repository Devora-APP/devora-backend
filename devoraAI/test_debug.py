import asyncio
from app.ai.debugger import run_debugger

code = """
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)):
        if n % i == 0:
            return False
    return True
"""

async def test():
    result = await run_debugger(code)
    with open("test_output.txt", "w", encoding="utf-8") as f:
        f.write(str(result))
    print("DEBUGGER RESULT written to test_output.txt")

if __name__ == "__main__":
    asyncio.run(test())
