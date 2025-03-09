import uuid
import asyncio
import httpx
import uvicorn

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

tasks: Dict[str, dict] = {}


class TaskRequest(BaseModel):
    urls: list[str]


class TaskResponse(BaseModel):
    task_id: str
    status: str
    results: list[dict[str, str]]


async def fetch_status(url: str) -> Dict[str, str]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5)
            return {"url": url, "status": str(response.status_code)}
        except httpx.RequestError:
            return {"url": url, "status": 'Error'}


async def process_task(task_id: str, urls: List[str]):
    results = await asyncio.gather(*(fetch_status(url) for url in urls))
    tasks[task_id]['status'] = 'ready'
    tasks[task_id]['results'] = results


@app.post("/api/v1/tasks/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(task: TaskRequest):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "running", "results": []}
    asyncio.create_task(process_task(task_id, task.urls))
    return {"task_id": task_id, "status": "running", "results": []}


@app.get("/api/v1/tasks/{received_task_id}")
async def get_task_status(received_task_id: str):
    if received_task_id not in tasks:
        raise HTTPException(status_code=404, detail='Task not found')
    return {"task_id": received_task_id, **tasks[received_task_id]}


@app.on_event('shutdown')
async def shutdown_event():
    print("Server is shutting down...")


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8888, reload=True)
