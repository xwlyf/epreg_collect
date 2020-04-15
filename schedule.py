# -*- coding: utf-8 -*-
from multiprocessing import Process
from db_connect import RedisDbConn
from crawl_basicinfo import EpregAppCollect
from crawl_detailinfo import DetailCollect
from config import *
import time
from loguru import logger


class Scheduler:

    def schedule_basic(self,cycle = BASCI_CYCLE):
        """
        定时采集企业的基本信息
        :param cycle:
        :return:
        """
        basic = EpregAppCollect()
        while True:
            count = RedisDbConn().get_count(INIT_STATUS, PARAMS_REDIS_DB)
            if count > 1000:
                logger.info("数据库已经有" + count + "的企业详细信息还未采集，基本信息采集暂停...")
                BASIC_ENABLED = False
            else:
                BASIC_ENABLED = True
            if BASIC_ENABLED:
                logger.info("开始抓取企业基本信息~~~~")
                basic.run()
            time.sleep(cycle)

    def schedule_detail(self,cycle=DETAIL_CYCLE):
        """
        采集企业详细信息
        :param cycle:
        :return:
        """

        getter = DetailCollect()
        while True:
            if GETTER_ENABLED:
                logger.info("开始抓取企业详细信息~~~~")
                getter.run()
            time.sleep(cycle)




    def run(self):
        logger.info("企业采集脚本开始运行~~~")


        test_process = Process(target=self.schedule_basic)
        test_process.start()
        # test_process.join()


        test_process = Process(target=self.schedule_detail)
        test_process.start()
        # test_process.join()



if __name__ == '__main__':
    spider = Scheduler()
    spider.run()