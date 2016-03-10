import redis

redis_store = redis.Redis()

KEY_PREFIX = 'WEME'

#community
COMMUNITY_KEY_PREFIX = "{}:community".format(KEY_PREFIX)
COMMUNITY_TOPIC_HOTINDEX_KEY = "{}:topic_hotindex".format(COMMUNITY_KEY_PREFIX)

def clear_redis():
	redis_store.delete(COMMUNITY_TOPIC_HOTINDEX_KEY)
