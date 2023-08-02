import asyncio
from dataclasses import dataclass
from typing import Dict

from fastapi import FastAPI, Depends
from starlette.websockets import WebSocket
import redis.asyncio as redis

app = FastAPI()


@dataclass
class UserInfo:
    id: int
    name: str
    score: int


users: Dict[int, UserInfo] = {
    1: UserInfo(1, "Amir", 12),
    2: UserInfo(2, "Alex", 15),
    3: UserInfo(2, "Sara", 9),
    4: UserInfo(2, "Sara", 9), #here
    5: UserInfo(2, "Sara", 9),
    6: UserInfo(2, "Sara", 9),
    7: UserInfo(2, "Sara", 9),
    8: UserInfo(2, "Sara", 9),
    9: UserInfo(2, "Sara", 9),
    10: UserInfo(2, "Sara", 9),
}

redis_connection_pool = redis.ConnectionPool()

def redis_connection() -> redis.Redis:
    return redis.Redis(connection_pool=redis_connection_pool)

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    await asyncio.sleep(0.2) # for exaggeration
    if user_id in users:
        return {"ok": True, "user": users[user_id]}
    return {"ok": False, "error": "user not founded"}

@app.get("/")
async def root():
    return {"hello": "world"}

@app.websocket("/ws")
async def ws_root(websocket: WebSocket, rdb: redis.Redis = Depends(redis_connection)):
    await websocket.accept()

    async def listen_redis():
        ps = rdb.pubsub()
        await ps.psubscribe("test_channel")
        
        while True:
            message = await ps.get_message(ignore_subscribe_messages=True, timeout=None)
            if message is None:
                continue
            text_message = message['data'].decode('utf-8')
            if text_message == "stop":
                await websocket.send_text("closing the connection")
                break
            await websocket.send_text(text_message)

    async def listen_ws():
        while True:
            message = await websocket.receive_text()
            await rdb.publish("test_channel", message)  # publishing the message to the redis pubsub channel


    await asyncio.wait([listen_ws(), listen_redis()], return_when=asyncio.FIRST_COMPLETED)

    # ps = rdb.pubsub()
    # await ps.psubscribe("test_channel")

    # while True:
    #     message = await ps.get_message(ignore_subscribe_messages=True, timeout=None)
    #     if message is None:
    #         continue
    #     text_message = message['data'].decode('utf-8')
    #     if text_message == "stop":
    #         await websocket.send_text("closing the connection")
    #         break
    #     await websocket.send_text(text_message)

    # await websocket.send_text("Hi")
    # if await rdb.ping():
    #     await websocket.send_text("connected to redis")

    await websocket.close()