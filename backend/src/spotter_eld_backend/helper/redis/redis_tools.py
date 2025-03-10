import logging
from functools import wraps

import redis
from django.conf import settings

log = logging.getLogger(__name__)

_pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD)


def get_connection():
    """
    Returns a redis connection. Make sure to close it after using it or just use it with the 'with' clause
    """

    return redis.Redis(connection_pool=_pool)


def redis_decoder(fn_to_wrap):
    """
    Decorator that decode values returned as dict or string
    """

    @wraps(fn_to_wrap)
    def wrapper(*args, **kwargs):

        byte_result = fn_to_wrap(*args, **kwargs)

        result = byte_result
        if byte_result is not None:

            if type(byte_result) == dict:
                result = {}
                for key, value in byte_result.items():
                    try:
                        result[key.decode("utf-8")] = value.decode("utf-8")
                    except:
                        result[key.decode("utf-8")] = value

            elif type(byte_result) == list:
                result = [u.decode("utf-8") for u in byte_result]

            else:
                try:
                    result = byte_result.decode("utf-8")
                except:
                    result = byte_result

        return result

    return wrapper


# ===============================================================================
# Data access functions
# ===============================================================================


@redis_decoder
def lrange(r_con, key, f, t):
    """
    Convert the returned value from byte to string
    """
    if not r_con:
        r_con = get_connection()

    return r_con.lrange(key, f, t)


@redis_decoder
def keys(r_con, key):
    """
    Convert the returned value from byte to string
    """
    if not r_con:
        r_con = get_connection()

    return r_con.keys(key)


@redis_decoder
def hgetall(r_con, name):
    """
    Convert the keys and values for byte to string
    """

    if not r_con:
        r_con = get_connection()

    result = r_con.hgetall(name)
    return result if result else {}


@redis_decoder
def hget(r_con, name, key):
    """
    Convert the returned value from byte to string
    """
    if not r_con:
        r_con = get_connection()

    return r_con.hget(name, key)


def get_hashed_document(name):
    """
    @return: return all the fields of the hashed document using hgetall(name). None if not found
    @param name: key of the hashed document in redis
    """

    return hgetall(None, name)


@redis_decoder
def rpop(r_con, name):
    """
    "Remove and return the last item of the list ``name``"
    Convert the returned value from byte to string
    """

    if not r_con:
        r_con = get_connection()

    return r_con.rpop(name)


@redis_decoder
def lpop(r_con, name):
    """
    "Remove and return the last item of the list ``name``"
    Convert the returned value from byte to string
    """

    if not r_con:
        r_con = get_connection()

    return r_con.lpop(name)


@redis_decoder
def get(r_con, name):
    """
    Return the value at key ``name``, or None if the key doesn't exist
    Convert the returned value from byte to string
    """

    if not r_con:
        r_con = get_connection()

    return r_con.get(name)


@redis_decoder
def rkeys(r_con, name):
    """
    Convert the returned value from byte to string
    """

    if not r_con:
        r_con = get_connection()

    result = r_con.keys(name)
    return result if result else []

