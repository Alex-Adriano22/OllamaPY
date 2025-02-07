from fastapi import FastAPI
from pydantic import BaseModel
import aiohttp  # Biblioteca para requisições assíncronas
import ollama
import asyncio  # Para rodar código síncrono em async

app = FastAPI()

DEFAULT_MODEL = "phi3"

class RequestModel(BaseModel):
    model: str = DEFAULT_MODEL  
    prompt: str

# 🔹 Chamada HTTP assíncrona ao Ollama
@app.post("/api/Ollama")
async def Gerar_texto_Api(request: RequestModel):
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": request.model,
        "prompt": request.prompt,
        "stream": False
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": "Falha ao chamar Ollama", "status_code": response.status}

# 🔹 Chamada direta ao Ollama usando async corretamente
@app.post("/api/ollama/Direto")
async def Gerar_texto(request: RequestModel):
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, ollama.generate, request.model, request.prompt)
    return {"response": response["response"]}
