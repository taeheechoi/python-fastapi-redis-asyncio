import asyncio
import time
from collections.abc import Callable
from typing import List

import aiohttp
import requests


def get_user_info(user_id: int) -> dict | None:
    response = requests.get(f"http://127.0.0.1:8000/user/{user_id}").json()
    if 'ok' not in response or not response['ok']:
        return None
    return response['user']

def combine_scores(ids: List[int]) -> None:
    users = [get_user_info(user_id) for user_id in ids]
    scores = [user['score'] for user in users if user is not None]
    print(sum(scores))


async def get_user_info_async(user_id: int) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://127.0.0.1:8000/user/{user_id}") as response:
            response = await response.json()
            if 'ok' not in response or not response['ok']:
                return None
            return response['user']

async def combine_scores_async(ids: List[int]) -> None:
    futures = [get_user_info_async(user_id) for user_id in ids]
    users = await asyncio.gather(*futures)
    scores = [user['score'] for user in users if user is not None]
    print(sum(scores))  

async def get_user_info_async(user_id: int) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://127.0.0.1:8000/user/{user_id}") as response:
            response = await response.json()
            if 'ok' not in response or not response['ok']:
                return None
            return response['user']

async def combine_scores_async(ids: List[int]) -> None:
    futures = [get_user_info_async(user_id) for user_id in ids]
    users = await asyncio.gather(*futures)
    scores = [user['score'] for user in users if user is not None]
    print(sum(scores))  

def run_and_analyze(method: Callable) -> None:
    start = time.time_ns()
    method()
    duration = time.time_ns() - start
    duration_ms = duration / 1_000_000
    print("took {}ms".format(duration_ms))

ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 


def test_sync():
    combine_scores(ids)

def test_async():
    asyncio.run(combine_scores_async(ids))


if __name__ == "__main__":
    print("Sync:")
    run_and_analyze(test_sync)
    print("Async:")
    run_and_analyze(test_async)