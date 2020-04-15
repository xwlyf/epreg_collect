# -*- coding: utf-8 -*-
from config import *
from utils import *
from db_connect import RedisDbConn,DbCollect
from loguru import logger
from cutent import *
from crawl_spider import *
import asyncio
import sys


class DetailCollect(object):
    def __init__(self):
        self.client = RedisDbConn()
        self.db = DbCollect()
        self.init_status = INIT_STATUS


    def run(self):
        try:
            count = self.client.get_count(self.init_status,PARAMS_REDIS_DB)
            logger.info("目前还剩余~~~~" + str(count) + "家企业的详细信息页未采集哦...")
            if count != 0:
                for i in range(count):
                    params_list = self.client.get_data(self.init_status,PARAMS_REDIS_DB)
                    if params_list:
                        loop = asyncio.get_event_loop()
                        tasks = [CrawlUrl().get_detailparams(params) for params in params_list]
                        loop.run_until_complete(asyncio.wait(tasks))
                        sys.stdout.flush()
                        time.sleep(random.randint(2, 5))
        except Exception as e:
            logger.debug("企业详细信息采集脚本发生错误" + str(e.args))



