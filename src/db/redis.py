import aioredis
from src.config import Config

JTI_EXPIRY = 3600

token_block_list = aioredis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0
)


async def add_jwi_to_blocklist(jti: str) -> None:
    await token_block_list.set(name=jti, value="", ex=JTI_EXPIRY)
