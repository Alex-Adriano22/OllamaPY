from fastapi import FastAPI
from pydantic import BaseModel
import requests
import ollama

app = FastAPI()

# Definindo um modelo padrão
DEFAULT_MODEL = "phi3"

# Modelo de entrada para a API
class RequestModel(BaseModel):
    model: str = DEFAULT_MODEL  # Define um valor padrão
    prompt: str

# Endpoint para chamar a API do Ollama via HTTP
@app.post("/api/generate")
def generate_text(request: RequestModel):
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": request.model,
        "prompt": request.prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Falha ao chamar Ollama", "status_code": response.status_code}

# Endpoint para chamar Ollama diretamente via Python
@app.post("/api/generate-ollama")
def generate_text_ollama(request: RequestModel):
    response = ollama.generate(model=request.model, prompt=request.prompt)
    return {"response": response["response"]}
