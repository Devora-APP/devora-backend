from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .ai.inquiry import run_inquiry
from .ai.debugger import run_debugger
import tempfile
import subprocess
import os
import uuid

app = FastAPI(title="DEVORA AI API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:3000", 
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InquiryRequest(BaseModel):
    prompt: str
    language: str = "auto"

class DebugRequest(BaseModel):
    code: str

class ExecuteRequest(BaseModel):
    code: str
    language: str = "python"

@app.get("/")
async def health_check():
    return {"status": "running", "message": "DEVORA API is live"}

@app.post("/api/v1/inquiry")
async def inquiry_endpoint(req: InquiryRequest):
    result = await run_inquiry(req.prompt, req.language)
    if "error" in result:
        raise HTTPException(status_code=422, detail=result["error"])
    return result

@app.post("/api/v1/debug")
async def debug_endpoint(req: DebugRequest):
    result = await run_debugger(req.code)
    if "error" in result:
        raise HTTPException(status_code=422, detail=result["error"])
    return result

@app.post("/api/v1/execute")
async def execute_endpoint(req: ExecuteRequest):
    lang = req.language.lower()
    
    # Map execution environments
    if lang in ["javascript", "js", "node"]:
        ext = ".js"
        cmd = ["node"]
    else:
        ext = ".py"
        cmd = ["python"]
        
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"devora_{uuid.uuid4().hex}{ext}")
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(req.code)
            
        cmd.append(file_path)
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=10.0, stdin=subprocess.DEVNULL)
        
        return {
            "output": process.stdout,
            "error": process.stderr,
            "exit_code": process.returncode
        }
    except subprocess.TimeoutExpired:
        return {"output": "", "error": "Execution timed out after 10 seconds. (Note: Infinite loops or very heavy operations will trigger this.)", "exit_code": -1}
    except Exception as e:
        return {"output": "", "error": str(e), "exit_code": -1}
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
