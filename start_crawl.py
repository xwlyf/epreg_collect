# -*- coding: utf-8 -*-
from crawl_basicinfo import EpregAppCollect
from schedule import Scheduler
from db_connect import RedisDbConn,DbCollect
import sys
import io
from loguru import logger
from config import *
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")

def main(keywords_list):
    """
    开始运行整个工商采集
    :return:
    """

    count = RedisDbConn().get_count(INIT_STATUS)
    if count == 0:
        if DELETE_REDIS_KEYWORDS and DELETE_REDIS_PARAMS:
            RedisDbConn().del_db(KEYWORDS_REDIS_DB)
            RedisDbConn().del_db(PARAMS_REDIS_DB)
        if SQL_INPUT:
            EpregAppCollect().entry_data()
        else:
            EpregAppCollect().add_keywords(keywords_list)
    else:
        logger.info("源redis库内已经有未采集的keywords.....")
    try:
        s = Scheduler()
        s.run()
    except Exception as e:
        logger.debug("开始采集出现问题--" + str(e.args))
        # main(keywords_list)


if __name__ == '__main__':
    keywords_list = ["启东","京东"]
    main(keywords_list)