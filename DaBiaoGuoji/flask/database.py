#连接mysql数据库专用,使用aiomysql插件
import sys
import asyncio
import logging
import aiomysql
logging.basicConfig(level=logging.INFO)
# 一次使用异步 处处使用异步  


def log(sql, args=()):
    logging.info('SQL:%s' % sql)


@asyncio.coroutine
def create_pool(loop, **kw):  # 这里的**kw是一个dict
    logging.info(' start creating database connection pool')
    global __pool
    # 理解这里的yield from 是很重要的  
    # dict有一个get方法，如果dict中有对应的value值，则返回对应于key的value值，否则返回默认值，例如下面的host，如果dict里面没有
    # 'host',则返回后面的默认值，也就是'localhost'
    # 这里有一个关于Pool的连接，讲了一些Pool的知识点，挺不错的，<a target="_blank" href="http://aiomysql.readthedocs.io/en/latest/pool.html">点击打开链接</a>，下面这些参数都会讲到，以及destroy__pool里面的
    # wait_closed()
    __pool = yield from aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw[''],
        password=kw[''],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),  # 默认自动提交事务，不用手动去提交事务
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )


@asyncio.coroutine
def destroy_pool():
    global __pool
    if __pool is not None:
        __pool.close()  # 关闭进程池,The method is not a coroutine,就是说close()不是一个协程，所有不用yield from
        yield from __pool.wait_closed()  # 但是wait_close()是一个协程，所以要用yield from,到底哪些函数是协程，上面Pool的链接中都有


# 我很好奇为啥不用commit 事务不用提交么？我觉得是因为上面再创建进程池的时候，有一个参数autocommit=kw.get('autocommit',True)
# 意思是默认会自动提交事务  
@asyncio.coroutine
def select(sql, args, size=None):
    log(sql, args)
    global __pool
    # 666 建立游标  
    # -*- yield from 将会调用一个子协程，并直接返回调用的结果  
    # yield from从连接池中返回一个连接， 这个地方已经创建了进程池并和进程池连接了，进程池的创建被封装到了create_pool(loop, **kw)  
    with (yield from __pool) as conn:  # 使用该语句的前提是已经创建了进程池，因为这句话是在函数定义里面，所以可以这样用
        cur = yield from conn.cursor(aiomysql.DictCursor)  # A cursor which returns results as a dictionary.
        yield from cur.execute(sql.replace('?', '%s'), args)
        if size:
            rs = yield from cur.fetchmany(size)  # 一次性返回size条查询结果，结果是一个list，里面是tuple
        else:
            rs = yield from cur.fetchall()  # 一次性返回所有的查询结果
        yield from cur.close()  # 关闭游标，不用手动关闭conn，因为是在with语句里面，会自动关闭，因为是select，所以不需要提交事务(commit)
        logging.info('rows have returned %s' % len(rs))
    return rs  # 返回查询结果，元素是tuple的list


# 封装INSERT, UPDATE, DELETE  
# 语句操作参数一样，所以定义一个通用的执行函数，只是操作参数一样，但是语句的格式不一样  
# 返回操作影响的行号  
# 我想说的是 知道影响行号有个叼用  

@asyncio.coroutine
def execute(sql, args, autocommit=True):
    log(sql)
    global __pool
    with (yield from __pool) as conn:
        try:
            # 因为execute类型sql操作返回结果只有行号，不需要dict  
            cur = yield from conn.cursor()
            # 顺便说一下 后面的args 别掉了 掉了是无论如何都插入不了数据的  
            yield from cur.execute(sql.replace('?', '%s'), args)
            yield from conn.commit()  # 这里为什么还要手动提交数据
            affected_line = cur.rowcount
            yield from cur.close()
            print('execute : ', affected_line)
        except BaseException as e:
            raise
        return affected_line

    # 这个函数主要是把查询字段计数 替换成sql识别的?


# 比如说：insert into  `User` (`password`, `email`, `name`, `id`) values (?,?,?,?)  看到了么 后面这四个问号
def create_args_string(num):
    lol = []
    for n in range(num):
        lol.append('?')
    return (','.join(lol))


# 定义Field类，负责保存(数据库)表的字段名和字段类型
class Field(object):
    # 表的字段包含名字、类型、是否为表的主键和默认值  
    def __init__(self, name, column_type, primary__key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary__key
        self.default = default

    def __str__(self):
        # 返回 表名字 字段名 和字段类型  
        return "<%s , %s , %s>" % (self.__class__.__name__, self.name, self.column_type)
    # 定义数据库中五个存储类型


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)
    # 布尔类型不可以作为主键


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'Boolean', False, default)
    # 不知道这个column type是否可以自己定义 先自己定义看一下


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'int', primary_key, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'float', primary_key, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)