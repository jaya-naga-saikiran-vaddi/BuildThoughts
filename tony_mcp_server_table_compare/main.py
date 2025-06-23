from fastapi import FastAPI
from pydantic import BaseModel
from mcp_server.controller import run_comparison_job

app = FastAPI()


class JobRequest(BaseModel):
    goal: str
    table_name: str


@app.post("/run-job")
async def run_job(request: JobRequest):
    trace = run_comparison_job(request.goal, request.table_name)
    return {"goal": request.goal, "trace": trace}
