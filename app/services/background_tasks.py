from arq.connections import RedisSettings
from typing import Any
import asyncio


async def send_email_task(ctx: dict[str, Any], email: str, subject: str, body: str):
    await asyncio.sleep(1)
    print(f"Sending email to {email}: {subject}")
    return {"status": "sent", "email": email}


async def process_user_task(ctx: dict[str, Any], user_id: str):
    await asyncio.sleep(1)
    print(f"Processing user {user_id}")
    return {"status": "processed", "user_id": user_id}


class WorkerSettings:
    functions = [send_email_task, process_user_task]

