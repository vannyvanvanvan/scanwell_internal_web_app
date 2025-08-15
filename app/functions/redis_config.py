import redis
# update the port if changed
redis_client = redis.Redis(host="localhost", port=32769, db=0, decode_responses=True)