import redis

rds = redis.StrictRedis(host='localhost', port=6379, db=0)
rds.flushdb()
rds.set('key', 0)
int(rds.get('key').decode())