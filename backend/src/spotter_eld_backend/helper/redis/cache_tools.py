import logging
import pickle

from django.core import serializers

from helper.redis import redis_tools

log = logging.getLogger(__name__)

# set to false to bypass the cache
use_cache = True

redis_con = redis_tools.get_connection()
def get_from_map(key, cache_map, fnIfNotFound):
    """
     Returns the value associated with 'key' in 'cache_map'. If not found it calls fnIfNotFound, fills it in cache_map the returns it
     @param key: key for the cached object
     @param cache_map: map used to cache objects
     @param fnIfNotFound: function to be called without parameters if key not found
    """

    if use_cache and key in cache_map:
        rt = cache_map.get(key)
    else:
        rt = fnIfNotFound()
        cache_map[key] = rt

    return rt


def get_model_from_redis_only(key):
    """
    @param key: the key to get the model from
    @param redis_conn: the redis connection to use
    @return: the deserialized object from redis
    """
    rt = []
    obj = redis_con.get(key)
    if obj:
        dObj = serializers.deserialize('json', obj)
        if dObj:
            for d in dObj:
                rt.append(d.object)

    return rt


def get_model_from_redis(key, fnIfNotFound, timeout_sec):
    """
     Returns the value associated with 'key' in the redis DB. The returned/stored in redis objects are django model objects.
     For JSON serializable objects use get_from_redis.
     It calls the fnIfNotFound, get the object or list, serialize to JSON and store it in a record like {'is_list':True, 'payload':<serialized data>}.
     it uses the is_list while deserializing from the cache to return it to the same type returned from fnIfNotFound

     On each call, it resets the timeout to 'timeout_sec'

     @param key: string key for the cached object. better to follow redis key structure e.g. cache:model:employee:<emp id>
     @param fnIfNotFound: function to be called without parameters if key not found. it should return either a QuerySet or an iterable object of type [django.db.Model]
     @param timeout_sec: timeout seconds
     @param redis_con: redis connection to be used
     @return: list of django.db.Model instances
    """

    obj = redis_con.get(key)
    if obj is None or not use_cache:
        obj = fnIfNotFound()

        dObj = serializers.serialize('json', obj)
        redis_con.set(key, dObj, ex=timeout_sec)

        # reread from redis in order to always return the same type
        obj = redis_con.get(key)

    redis_con.expire(key, timeout_sec)

    dObj = serializers.deserialize('json', obj)
    rt = []
    for d in dObj:
        rt.append(d.object)

    return rt


def get_from_redis(key, fnIfNotFound, timeout_sec):
    """
    Returns the value associated with 'key' in the redis DB.
    The return result of fnIfNotFound should serializable via json.dumps. To cache django.Models then use get_model_from_redis.
    On each call, it resets the timeout to 'timeout_sec'

     @param key: string key for the cached object. better to follow redis key structure e.g. cache:store:<store_code>:data_name
     @param fnIfNotFound: function to be called without parameters if key not found. it should return either a QuerySet or an iterable object of type [django.db.Model]
     @param timeout_sec: timeout seconds
     @param redis_con: redis connection to be used
     @return: deserialized object as returned by fnIfNotFound
    """

    obj = redis_con.get(key)
    if obj is None or not use_cache:
        obj = fnIfNotFound()

        dObj = pickle.dumps(obj)
        redis_con.set(key, dObj, ex=timeout_sec)

        # reread from redis in order to always return the same type
        obj = redis_con.get(key)

    redis_con.expire(key, timeout_sec)
    rt = pickle.loads(obj)

    return rt


def purge_cache(keys):
    """
    Removes the given key from the cache.
    @param keys: array of keys to purge
    """
    log.debug("Purging cache for: %s", keys)
    if keys:
        redis_con.delete(*keys)
