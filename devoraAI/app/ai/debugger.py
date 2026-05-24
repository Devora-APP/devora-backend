import re
from .llm_client import call_ollama

def detect_language(code: str) -> str:
    try:
        from guesslang import Guess
        guess = Guess()
        lang = guess.language_name(code)
        return lang if lang else "unknown"
    except Exception:
        return "unknown"

async def run_debugger(code: str) -> dict:
    detected_lang = detect_language(code)
    
    system_prompt = """You are an elite debugging machine. Analyze the code, find the bugs, and provide the exact fixed code.
You MUST output ONLY a valid JSON object wrapped in exactly one markdown code block (```json ... ```) matching this schema perfectly:
{
  "language": "python",
  "errors": [
    {"line": 2, "type": "SyntaxError", "explanation": "Missing parentheses"}
  ],
  "fixed_code": "the full corrected source code",
  "changes": [
    {"original": "bad code snippet", "fixed": "good code", "reason": "why"}
  ],
  "summary": "overall summary"
}
"""
    user_prompt = f"Please debug the following code:\n\n```{detected_lang}\n{code}\n```"
    
    try:
        content = await call_ollama(system_prompt, user_prompt)
        
        # Remove deepseek-r1 thinking block if present
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
        
        # Extract markdown json securely
        import json
        match = re.search(r'```(?:json)?\n?(.*?)\n?```', content, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            # Failsafe cleaner for trailing commas
            json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
            try:
                data = json.loads(json_str)
                return {
                    "language": data.get("language", detected_lang),
                    "fixed_code": data.get("fixed_code", code),
                    "errors": data.get("errors", []),
                    "changes": data.get("changes", []),
                    "summary": data.get("summary", "Debugging complete.")
                }
            except json.JSONDecodeError:
                pass
                
        # If JSON parsing completely fails, fallback to raw format
        fixed_code = code
        summary = content
        raw_match = re.search(r'```(?:\w+)?\n(.*?)```', content, re.DOTALL)
        if raw_match:
            fixed_code = raw_match.group(1).strip()
            summary = content.replace(raw_match.group(0), "").strip()
            
        return {
            "language": detected_lang,
            "fixed_code": fixed_code,
            "errors": [{"line": 0, "type": "ParseWarning", "explanation": "The AI provided a fix but the diff failed to render. See full code."}],
            "changes": [],
            "summary": summary
        }
    except Exception as e:
        return {"error": str(e)}
