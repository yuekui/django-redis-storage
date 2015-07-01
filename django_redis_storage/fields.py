import itertools
from django.conf import settings
from django.core.files.storage import Storage

from redis import Redis
from .file import RedisFile


class RedisStorage(Storage):
    _redis_connection = None

    def __init__(self, host='localhost', port=6379,
                 db=0, password=None, socket_timeout=None,
                 connection_pool=None, charset='utf-8',
                 errors='strict', decode_responses=False,
                 unix_socket_path=None):
        """

        @param host:
        @type host: str
        @param port:
        @type port: int
        @param db:
        @type db:int
        @param password:
        @type password: str
        @param socket_timeout:
        @param connection_pool:
        @param charset:
        @param errors:
        @param decode_responses:
        @param unix_socket_path:
        """
        self._redis_connection = Redis(host, port, db, password, socket_timeout, connection_pool, charset, errors,
                                       decode_responses, unix_socket_path)

    def _open(self, name, *args, **kwargs):
        return RedisFile(name, redis_connection=self._redis_connection)

    def _save(self, name, content):
        redis_file = RedisFile(name, redis_connection=self._redis_connection)
        redis_file.writelines(content)
        return name

    def get_valid_name(self, name):
        return name

    def get_available_name(self, name):
        while self.exists(name):
            count = itertools.count(1)
            name = u'{0}_{1}'.format(name, count)
        return name

    def url(self, name):
        return u''

    def exists(self, name):
        return self._redis_connection.exists(name)

    def delete(self, name):
        self._redis_connection.delete(name)
