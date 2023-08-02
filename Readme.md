- uvicorn main:app --reload
- docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
- docker exec -it redis-stack redis-cli

### References

- https://medium.com/itnext/scalable-real-time-apps-with-python-and-redis-exploring-asyncio-fastapi-and-pub-sub-79b56a9d2b94
- https://redis.io/docs/getting-started/install-stack/docker/
