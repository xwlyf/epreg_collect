# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent
import json
from config import *
eplisturl = "https://app.gsxt.gov.cn/gsxt/cn/gov/saic/web/controller/PrimaryInfoIndexAppController/search?page=1"
params = {"searchword": "%s" % "天堂",
                      "conditions": {"excep_tab": "0", "ill_tab": "0", "area": "%s" % AREA, "cStatus": "0", "xzxk": "0",
                                     "xzcf": "0", "dydj": "0"}, "sourceType": "I"}
data = json.dumps(params, ensure_ascii=False).encode("utf-8")
def get_header():
    """
    获取请求头
    :return: headers
    """
    headers = {
        'Host': 'app.gsxt.gov.cn',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': "%s" % UserAgent().random,
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'br, gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        # "Cookie": "JSESSIONID=4C6FF8B7C0F33C70405FD78CF50E2E2B; tlb_cookie=172.16.12.1128080; SECTOKEN=7143533173465156583; __jsluid=6965c755d93b890835c56808a4ace4da"
    }
    return headers
# data = b'{"searchword": "\xe5\xa4\xa9\xe5\xa0\x82", "conditions": {"excep_tab": "0", "ill_tab": "0", "area": "120000", "cStatus": "0", "xzxk": "0", "xzcf": "0", "dydj": "0"}, "sourceType": "I"}'
req = requests.post(eplisturl,headers=get_header(),timeout=10,data=data)
print(req.text)