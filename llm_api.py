import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from local_llm_handler import local_llm  # Reuse your existing handler

app = FastAPI(title="ForeverFit AI API", description="API for Fine-tuned Local LLM")

class GenerateRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    max_tokens: Optional[int] = 1024  # Increased for detailed responses
    temperature: Optional[float] = 0.85  # Higher for more creative, expert-like responses

@app.get("/health")
def health_check():
    if local_llm.model:
        return {"status": "valid", "model": "DeepSeek-R1-Distill-Qwen-7B + LoRA"}
    return {"status": "loading_or_failed"}

@app.post("/generate")
async def generate(request: GenerateRequest):
    """Non-streaming generation endpoint"""
    try:
        response = local_llm.generate_response(
            system_prompt=request.system_prompt,
            user_prompt=request.user_prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_stream")
async def generate_stream(request: GenerateRequest):
    """Streaming generation endpoint using SSE"""
    
    async def event_generator():
        try:
            # We iterate over the synchronous generator from local_llm
            # In a real async app, we might want to run this in a threadpool if it blocks,
            # but local_llm.generate_response_stream already uses a separate thread for model.generate
            # so the iteration itself is just waiting for the queue.
            
            stream = local_llm.generate_response_stream(
                system_prompt=request.system_prompt,
                user_prompt=request.user_prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            for token in stream:
                # SSE format: "data: <content>\n\n"
                # We yield strictly data messages
                yield {"data": token}
                # Minimal sleep to allow event loop breathing if needed, though usually not required for queue reads
                await asyncio.sleep(0)
                
            yield {"data": "[DONE]"}
            
        except Exception as e:
            yield {"event": "error", "data": str(e)}

    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    # Run on 0.0.0.0 to be accessible from other machines
    uvicorn.run(app, host="0.0.0.0", port=8000)
