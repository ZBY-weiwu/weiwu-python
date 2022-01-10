# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/15

import time

import pymysql
import redis
from redis import exceptions
from pymysql.err import Error
from dbutils.pooled_db import PooledDB


class ShortConnectMySQL(object):
    def __init__(self, host, user, passwd, db, port=3306, charset='utf8', **kwargs):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        self.kwargs = kwargs
        self.conn = None
        self.cursor = None
        self.connect()
        self.set_cursor()

    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.passwd, database=self.db,
                                        port=self.port, charset=self.charset, **self.kwargs)
            return True
        except Exception as e:
            print(e)
            return False

    def reconnect(self, try_count=1024, try_interval=3):
        if self.is_connected():
            return True
        has_try = 0
        while has_try < try_count:
            try:
                self.conn.ping()
                return True
            except Exception as e:
                has_try += 1
                time.sleep(try_interval)
        else:
            return False

    def is_connected(self):
        if not self.conn:
            return False
        return not self.conn._closed

    def set_cursor(self):
        if not self.conn:
            return False
        try:
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            return True
        except Exception as e:
            print(e)
            return False

    def select(self, sql, long='short'):
        self.reconnect()
        self.set_cursor()
        if not self.conn or not self.cursor:
            return False
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(e)
            return False
        finally:
            self.cursor_close()
            if long == 'short':
                self.connect_close()

    def modify(self, sql, long='short'):
        self.reconnect()
        self.set_cursor()
        if not self.conn or not self.cursor:
            return False
        try:
            if isinstance(sql, list):
                for _sql in sql:
                    self.cursor.execute(sql)
            else:
                self.cursor.execute(sql)
            self.conn.commit()
            return True
        except pymysql.err.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        except Exception as e:
            self.conn.rollback()
            return False
        finally:
            self.cursor_close()
            if long == 'short':
                self.connect_close()

    def modify_many(self, sql, sql_args, long='short'):
        self.reconnect()
        self.set_cursor()
        if not self.conn or not self.cursor:
            return False
        try:
            self.cursor.executemany(sql, sql_args)
            self.conn.commit()
            return True
        except pymysql.err.IntegrityError as e:
            print(e)
            self.conn.rollback()
            return False
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            self.cursor_close()
            if long == 'short':
                self.connect_close()

    def cursor_close(self):
        if not self.cursor:
            return
        try:
            self.cursor.close()
        except Exception as e:
            pass

    def connect_close(self):
        if not self.conn:
            return
        try:
            self.conn.close()
        except Error:
            pass


class LengthConnectMySQL(ShortConnectMySQL):
    def select(self, sql, long='length'):
        return super(LengthConnectMySQL, self).select(sql, long)

    def modify(self, sql, long='length'):
        return super(LengthConnectMySQL, self).modify(sql, long)

    def modify_many(self, sql, sql_args, long='length'):
        return super(LengthConnectMySQL, self).modify_many(sql, sql_args, long)


class MySQLPooled(object):
    def __init__(self, pool_kwargs, enable=False):
        self.pool = None
        if enable:
            try:
                self.pool = PooledDB(creator=pymysql, **pool_kwargs)
            except pymysql.err.OperationalError:
                print('数据库连接失败......')


class MySQLPooledHandler(object):
    """
    一个对象对应一个连接，同一个对象不能给多线程使用，而是使用多个对象(使用同一个PooledDB)来实现多线程
    """

    def __init__(self, pooled, cursor_type=None):
        self.pool = pooled.pool
        self.conn = None
        self.cursor = None
        self.cursor_type = cursor_type

    def fetchone(self, query, args=None):
        self.__connect()
        self.__execute(query, args)
        result = self.cursor.fetchone()
        self.__close()
        return result

    def fetchall(self, query, args=None):
        self.__connect()
        self.__execute(query, args)
        result = self.cursor.fetchall()
        self.__close()
        return result

    def fetchmany(self, query, args=None, size=None):
        self.__connect()
        self.__execute(query, args)
        result = self.cursor.fetchmany(size)
        self.__close()
        return result

    def execute(self, query, args=None, rollback=True):
        self.__connect()
        result = self.cursor.execute(query, args)
        if rollback:
            self.commit_rollback()
        else:
            self.commit()
        self.__close()
        return result

    def executemany(self, query, args, rollback=True):
        self.__connect()
        result = self.cursor.executemany(query, args)
        if rollback:
            self.commit_rollback()
        else:
            self.commit()
        self.__close()
        return result

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def commit_rollback(self):
        try:
            self.commit()
        except Exception as e:
            print(e)
            self.rollback()

    def __execute(self, query, args=None):
        try:
            result = self.cursor.execute(query, args)
            return result
        except Exception as e:
            print(e)

    def __executemany(self, query, args):
        try:
            result = self.cursor.executemany(query, args)
            return result
        except Exception as e:
            print(e)

    def __connect(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(self.cursor_type)

    def __close(self):
        self.cursor.close()
        self.conn.close()


class Redis(redis.Redis):
    pass


class RedisQueueScheduler(object):
    def __init__(self, redis_kwargs=None, locked=True, lock_kwargs=None):
        if redis_kwargs is None:
            redis_kwargs = {}
        self.locked = locked
        if lock_kwargs is None:
            lock_kwargs = {}
        self.lock_kwargs = lock_kwargs
        self.redis = Redis(**redis_kwargs)

    def _lock(self, func, lock_kwargs=None, **kwargs):
        if lock_kwargs is None:
            lock_kwargs = self.lock_kwargs
        if not lock_kwargs.get('name', None):
            lock_kwargs['name'] = '%s_lock' % kwargs['name']
        lock_kwargs['blocking_timeout'] = 3
        data = list()
        try:
            with self.redis.lock(**lock_kwargs) as lock:
                data = func(**kwargs)
        except exceptions.LockError as e:
            self.redis.delete(lock_kwargs['name'])
        return data

    def get(self, name, max_size=1024, policy='l', trim=False, locked=None, lock_kwargs=None):
        if locked is None:
            locked = self.locked
        if locked:
            return self._lock(self._get, lock_kwargs=lock_kwargs, name=name,
                              max_size=max_size, policy=policy, trim=trim)
        else:
            return self._get(name, max_size, policy, trim)

    def _get(self, name, max_size=1024, policy='l', trim=True):
        get_start = 0
        get_end = get_start + max_size - 1
        trim_start = max_size
        trim_end = -1
        if policy != 'l':
            index = self.qsize(name) - max_size
            index = index if index > 0 else 0
            get_start = index
            get_end = -1
            trim_start = 0
            trim_end = index - 1 if index > 0 else 0
        result = self.redis.lrange(name, get_start, get_end)
        if trim:
            self.redis.ltrim(name, trim_start, trim_end)
        return result

    def put(self, name, values, policy='l', locked=None, lock_kwargs=None):
        if locked is None:
            locked = self.locked
        if locked:
            return self._lock(self._put, lock_kwargs=lock_kwargs, name=name, policy=policy, values=values)
        else:
            return self._put(name, values, policy)

    def _put(self, name, values, policy):
        if policy == 'l':
            self.redis.lpush(name, *values)
        else:
            self.redis.rpush(name, *values)


    def qsize(self, name):
        return self.redis.llen(name)


def get_mysql_pool_handler(pool_kwargs, enable=False, cursor_type=None):
    mysql_db = MySQLPooled(pool_kwargs=pool_kwargs, enable=enable)
    return MySQLPooledHandler(mysql_db, cursor_type=cursor_type)


if __name__ == '__main__':
    pool = MySQLPooled(pool_kwargs={
        'mincached': 2,
        'maxcached': 5,
        'maxconnections': 10,
        'host': '10.1.101.53',
        'user': 'root',
        'password': '',
        'database': 'wemedia'
    })
    mysql_helper = MySQLPooledHandler(pool)
    mysql_helper1 = MySQLPooledHandler(pool)
    print(mysql_helper.fetchone('select * from user_1h', ))
    print(mysql_helper1.fetchone('select * from user_1h', ))
