import asyncio
import aiohttp
from faker import Faker

async def create_task():
    fake = Faker()

    task_data = {
        "name": fake.word(),
        "type": fake.word(),
        "created_at": fake.iso8601(),
        "status": fake.word()
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5000/tasks', json=task_data) as response:
            if response.status == 200:
                print("Task created successfully.")
            else:
                print("Failed to create task.")

asyncio.run(create_task())