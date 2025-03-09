import uuid
import asyncio
import httpx
import uvicorn
import redis.asyncio as Redis

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List
from urllib.parse import urlparse


REDIS_HOST = "localhost"
REDIS_PORT = 6379
CACHE_TTL = 60
redis = None
app = FastAPI()
tasks: Dict[str, dict] = {}


@app.on_event('startup')
async def startup_event():
    global redis
    redis = await Redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)
    asyncio.create_task(cleanup_cache())


@app.on_event('shutdown')
async def shutdown_event():
    print("Server is shutting down...")
    redis.aclose()


class TaskRequest(BaseModel):
    urls: list[str]


class TaskResponse(BaseModel):
    task_id: str
    status: str
    results: list[dict[str, str]]


async def fetch_status(url: str) -> Dict[str, str]:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    cached_status = await redis.get(f"matrix:cache:{url}")
    if cached_status:
        return {"url": url, "status": str(cached_status)}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5)
            status_code = str(response.status_code)
        except httpx.TimeoutException:
            return {"url": url, "status": 'Timeout'}
        except httpx.RequestError:
            return {"url": url, "status": 'Error'}

    await redis.setex(f'matrix:cache:{url}', CACHE_TTL, status_code)
    await redis.incr(f'matrix:count:{domain}')

    return {"url": url, "status": str(response.status_code)}


async def process_task(task_id: str, urls: List[str]):
    results = await asyncio.gather(*(fetch_status(url) for url in urls))
    tasks[task_id]['status'] = 'ready'
    tasks[task_id]['results'] = results


async def cleanup_cache():
    while True:
        await asyncio.sleep(CACHE_TTL/10)
        all_keys = await redis.keys(f'matrix:cache:*')
        for key in all_keys:
            ttl = await redis.ttl(key)
            if ttl == -2:
                await redis.delete(key)
        print("Cache cleanup done.")


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


@app.get("/api/v1/domain-count/{domain}")
async def get_domain_count(domain: str):
    count = await redis.get(f"matrix:count:{domain}")
    return {"domain": domain, "count": int(count) if count else 0}


@app.get("/api/v1/domain-count/")
async def get_domain_count_all():
    ret = []
    all_doms = await redis.keys(f'matrix:count:*')
    for key in all_doms:
        domain = key.split("matrix:count:")[-1]
        count = await redis.get(key)
        ret.append({"domain": domain, "count": int(count)})
    return ret


if __name__ == "__main__":
    uvicorn.run("server_cached:app", host="127.0.0.1", port=8888, reload=True)
