# -*- coding: utf-8 -*-

# redis 配置
REDIS_HOST = "localhost"
REDIS_PORT = 6379
KEYWORDS_REDIS_DB = "keywords"
PARAMS_REDIS_DB = "params"


# mysql 配置
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "app_collect"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"


AREA = "120000" # 行政区划代码


INIT_STATUS = 0
SUCCESS_STATUS = 1
FAILURE_STATUS = 2


VALID_STATUS_CODE = [200]

# BATCH_TEST_SIZE = 50


BASCI_CYCLE = 300 # 5循环遍历一次
DETAIL_CYCLE = 300 # 5遍历一次


BASIC_ENABLED = True
GETTER_ENABLED = True


MAX_WORKERS = 5  # 并行最大数

