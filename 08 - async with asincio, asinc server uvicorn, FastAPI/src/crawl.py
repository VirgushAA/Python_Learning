import asyncio
import httpx
import sys

SERVER_URL = "http://127.0.0.1:8888"


async def submit_task(urls):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{SERVER_URL}/api/v1/tasks/', json={'urls': urls})
        print(response.raise_for_status())
        return response.json()['task_id']


async def poll_task(task_id):
    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(f'{SERVER_URL}/api/v1/tasks/{task_id}')
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'ready':
                return data['results']
            await asyncio.sleep(1)


async def main():
    if len(sys.argv) < 2:
        print('Usage: python crawl.py <URL1> <URL2> ...')
        return

    urls = sys.argv[1:]
    task_id = await submit_task(urls)
    print(f"Task submitted: {task_id}, waiting for results...")

    result = await poll_task(task_id)
    for item in result:
        print(f"{item['status']}\t{item['url']}")


if __name__ == '__main__':
    asyncio.run(main())
