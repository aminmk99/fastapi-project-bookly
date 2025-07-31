import aioredis
from src.config import Config

token_block_list = aioredis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0
)
