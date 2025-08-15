from fastapi import FastAPI
from pydantic import BaseModel
from Agent import agent  # import your agent function from wherever you keep it
import startup
app = FastAPI(title="KrishiMitra Agent API")

# Request body schema
class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "KrishiMitra Agent API is running!"}

@app.post("/agent")
def run_agent(request: QueryRequest):
    try:
        result = agent(request.query)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}
