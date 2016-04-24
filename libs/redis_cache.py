import redis
import simplejson
import traceback
import os

REDIS_HOST = "ec2-54-83-34-248.compute-1.amazonaws.com"
REDIS_PORT = 11209
REDIS_PASS = 'pvc0s3mj8bjj9em016172mohj9'
REDIS_URL = "redis://h:pvc0s3mj8bjj9em016172mohj9@ec2-54-83-34-248.compute-1.amazonaws.com:11209"

REDIS_DB_TEMPLATE = {
    "tasks":{},
    "last_id":0
}

class CacheService:
    def __init__(self):
        print "start redis init"
        #self.r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASS, ssl=True)
        self.r = redis.from_url(REDIS_URL)
        print "end redis init"

    def ping(self):
        # Ping cache server
        return self.r.ping()

    def get(self, key):
        # Get value by key from cache
        try:
            resxult = self.r.get(key)
            return resxult
        except:
            print "Error on redis get"
            print traceback.format_exc()
            return None

    def set(self, key, value):
        # Save value to cache
        return self.r.set(key, value)

    def delete(self, key):
        # Save value to cache
        return self.r.delete(key)

    def get_db(self):
        result = self.get("REDES_DB")
        if result is None:
            return  REDIS_DB_TEMPLATE
        return simplejson.loads(result)

    def save_db(self, db):
        db_string = simplejson.dumps(db)
        try:
            self.set("REDES_DB", db_string)
        except:
            print "Error on redis write"
            print traceback.format_exc()
