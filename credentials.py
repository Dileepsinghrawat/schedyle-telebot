import os
import redis
token = os.environ['TELEGRAM_TOKEN']
admins = [os.environ['ADMIN1'], os.environ['ADMIN2']]
r = redis.from_url(os.environ.get("REDIS_URL"))
