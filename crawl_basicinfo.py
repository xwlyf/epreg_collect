# -*- coding: utf-8 -*-
from config import *
from utils import *
from db_connect import RedisDbConn,DbCollect
from loguru import logger
from cutent import *
import sys
from crawl_spider import *


class EpregAppCollect(object):
    def __init__(self):
        self.client = RedisDbConn()
        self.db = DbCollect()
        self.init_status = INIT_STATUS
        self.cut = CutEntername()

    def entry_data(self):
        """
        将原有的mysql数据库内的keywords放进redis有序集合中
        :return:
        """
        keywords_list = self.db.connect_db()
        for keyword in keywords_list:
            self.client.initial_set(keyword)


    def add_keywords(self,keywords_list):
        """
        可以实现自己手动增加keywords
        :param keywords_list: 传入的是keywords 列表
        :return:
        """
        for keyword in keywords_list:
            self.client.initial_set(keyword)

    def run(self):
        try:
            count = self.client.get_count(self.init_status)
            logger.info("目前还剩余~~~~" + str(count) + "个keywords未采集哦...")
            if count != 0:
                for i in range(count):
                    keyword_list = self.client.get_data(self.init_status)
                    if keyword_list:
                        for params in CrawlUrl().get_params(keyword_list):
                            self.cut.cutentername(params["entName"])
                        sys.stdout.flush()
                        time.sleep(random.randint(2, 5))
        except Exception as e:
            logger.debug("采集脚本发生错误" + str(e.args))



