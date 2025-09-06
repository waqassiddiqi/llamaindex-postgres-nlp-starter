from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .sql_engine import ask_sql


app = FastAPI(title="LlamaIndex NL→SQL Demo")


class Ask(BaseModel):
    question: str


@app.post("/ask-sql")
def ask_sql_api(req: Ask):
    try:
        return ask_sql(req.question)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))