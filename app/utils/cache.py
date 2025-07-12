import json
import pickle
from typing import Any, Optional, Union
from datetime import timedelta
import redis.asyncio as aioredis
from config import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)

class CacheService:
    """Redis-based caching service for improving performance"""
    
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
        self._connect()
    
    def _connect(self):
        """Connect to Redis if URL is provided"""
        if settings.redis_url:
            try:
                self.redis = aioredis.from_url(
                    settings.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
                logger.info("Connected to Redis cache")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}")
                self.redis = None
        else:
            logger.info("Redis not configured, caching disabled")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis:
            return None
        
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: Optional[timedelta] = None) -> bool:
        """Set value in cache with optional expiration"""
        if not self.redis:
            return False
        
        try:
            serialized_value = json.dumps(value, default=str)
            await self.redis.set(key, serialized_value, ex=expire.total_seconds() if expire else None)
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self.redis:
            return False
        
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    async def delete_pattern(self, pattern: str) -> bool:
        """Delete all keys matching a pattern"""
        if not self.redis:
            return False
        
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                await self.redis.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Cache delete pattern error for {pattern}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.redis:
            return False
        
        try:
            return await self.redis.exists(key) > 0
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False
    
    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment a counter in cache"""
        if not self.redis:
            return None
        
        try:
            return await self.redis.incr(key, amount)
        except Exception as e:
            logger.error(f"Cache increment error for key {key}: {e}")
            return None

class CacheDecorator:
    """Decorator for caching function results"""
    
    def __init__(self, cache_service: CacheService, prefix: str = "", expire: timedelta = timedelta(hours=1)):
        self.cache_service = cache_service
        self.prefix = prefix
        self.expire = expire
    
    def __call__(self, func):
        import functools
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{self.prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = await self.cache_service.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await self.cache_service.set(cache_key, result, self.expire)
            logger.debug(f"Cached result for {cache_key}")
            
            return result
        
        return wrapper

# Initialize cache service
cache_service = CacheService()

# Common cache decorators
def cache_user_data(expire: timedelta = timedelta(hours=1)):
    """Cache decorator for user-related data"""
    return CacheDecorator(cache_service, prefix="user", expire=expire)

def cache_training_data(expire: timedelta = timedelta(minutes=30)):
    """Cache decorator for training-related data"""
    return CacheDecorator(cache_service, prefix="training", expire=expire)

def cache_exercise_data(expire: timedelta = timedelta(hours=2)):
    """Cache decorator for exercise-related data"""
    return CacheDecorator(cache_service, prefix="exercise", expire=expire) 