import jieba
from collections import Counter
from db_connect import RedisDbConn
from loguru import logger
class CutEntername:
    def __init__(self):
        self.client = RedisDbConn()

    def cutentername(self,entername):
        """
        分词
        :param entername:
        :return: keyword
        """

        seg_list = jieba.cut(entername)
        logger.info("正在分词------" + entername)
        c = Counter()
        for x in seg_list:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1
        for (keyword, v) in c.most_common():
            if isinstance(keyword,str):
                if not self.client.exists_keyword(keyword):
                    self.client.initial_set(keyword)









