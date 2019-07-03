import redis
from sachima import conf


class Singleton(type):
    """
    An metaclass for singleton purpose. Every singleton class should inherit from this class by 'metaclass=Singleton'.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class RedisClient(metaclass=Singleton):
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=conf.get("REDIS_HOST"),
            port=conf.get("REDIS_PORT"),
            decode_responses=True,
            socket_connect_timeout=1
            # password=conf.get("REDIS_PASS"),
        )

    @property
    def conn(self):
        if not hasattr(self, "_conn"):
            self.getConnection()
        return self._conn

    def getConnection(self):
        self._conn = redis.StrictRedis(
            connection_pool=self.pool, charset="utf-8"
        )
