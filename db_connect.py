# -*- coding: utf-8 -*-
from config import *
import pymysql
import redis
import asyncio

class DbCollect:
    def __init__(self):
        self.db = MYSQL_DB
        self.user = MYSQL_USER
        self.passwd = MYSQL_PASSWORD
        self.host = MYSQL_HOST
        self.port = MYSQL_PORT
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.passwd, port=self.port, db=self.db,
                                    charset="utf8")
        self.cur = self.conn.cursor()
        self.client = RedisDbConn()

    def connect_db(self):
        """
        链接数据库，并且获取数据库内已有的keywords
        :return: 关键词列表 list
        """
        self.cur.execute("select keyword from qggs_app_keywords limit 100")
        keywords_list = [row[0] for row in self.cur.fetchall()]
        return keywords_list

    def insert_basicsql(self, tbname, params):
        """
        插入数据到数据库
        :param tbname: 要插入的数据表名称
        :param params: 字段的字典形式
        """
        self.client.initial_set(str(params),PARAMS_REDIS_DB)
        lists = [(k, params[k]) for k in params if params[k]]
        sentence = 'insert into %s (' % tbname + ','.join([i[0] for i in lists]) + ') values (' + ','.join(
            ['%r' % i[1] for i in lists]) + ');'
        self.cur.execute(sentence)

    async def insert_detailsql(self, tbname, params,ori_params):
        """
        插入数据到数据库
        :param tbname: 要插入的数据表名称
        :param params: 字段的字典形式
        """
        lists = [(k, params[k]) for k in params if params[k]]
        sentence = 'insert into %s (' % tbname + ','.join([i[0] for i in lists]) + ') values (' + ','.join(
            ['%r' % i[1] for i in lists]) + ');'
        self.cur.execute(sentence)
        self.client.set_success(PARAMS_REDIS_DB,ori_params)




class RedisDbConn:
    def __init__(self):
        self.client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

    def get_data(self, status,key=KEYWORDS_REDIS_DB):
        """
        判断redis中keywords
        :param status: 状态码
        :return: keywords list
        """
        return self.client.zrangebyscore(key, status, status)

    def get_count(self, status,key=KEYWORDS_REDIS_DB):
        """
        获取数量
        :param status: 状态码
        :return: 数量
        """
        return self.client.zcount(key, status, status)

    def exists_keyword(self, keyword,key=KEYWORDS_REDIS_DB):
        """
        判断关键词是否在库内
        :param keyword: 关键词
        :return: 值
        """
        return True if self.client.zrank(key, keyword) else False

    def set_success(self, keyword,key=KEYWORDS_REDIS_DB):
        """
        将keywords设置为已采集标签 1
        :param keyword: 关键字
        :return: 是否成功设置
        """
        if isinstance(keyword, str):
            self.client.zadd(key, {keyword: SUCCESS_STATUS})
            return True

    def set_failure(self, keyword,key=KEYWORDS_REDIS_DB):
        """
        将keywords设置为已失败采集标签 2
        :param keyword: 关键字
        :return: 是否成功设置
        """
        if isinstance(keyword, str):
            self.client.zadd(key, {keyword: FAILURE_STATUS})
            return True

    def initial_set(self, keyword,key=KEYWORDS_REDIS_DB):
        """
        初始化设置，新进来的keywords设置为 0 未采集标签
        :param keyword: 关键字
        :return: 是否成功设置
        """
        if not self.client.zscore(key, keyword):
            self.client.zadd(key, {keyword: INIT_STATUS})
            return True


    def batch_keyword(self,start,stop,key=KEYWORDS_REDIS_DB):
        """
        批量获取关键词，指定前几个
        :param start: 开始索引
        :param end: 结束索引
        :return: 关键词列表
        """
        result = self.client.zrevrange(key,start,stop)
        return result