# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
import requests
import chardet
import time
from loguru import logger
from config import *
import random
import aiohttp
import asyncio

semaphore = asyncio.Semaphore(MAX_WORKERS)
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


def get_headers2():
    header2 = {
        'Host': 'app.gsxt.gov.cn',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'file: //',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': "%s" % UserAgent().random,
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'br, gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest'
    }
    return header2


def req_data(url,data,page,keyword,timeout=10,proxies=None):
    """
    用来请求采集网址
    :param data: 请求参数
    :param url: url
    :param page: 页数
    :param keyword: 关键词
    :return: html
    """
    count = 1
    while count < 6:
        try:
            req = requests.post(url+str(page),headers=get_header(),timeout=timeout,data=data)
            if req.status_code in VALID_STATUS_CODE and len(req.text) > 100:
                return req.text
            else:
                # logger.error("正在重试请求 第" +  str(count) + "次" )
                count += 1
                time.sleep(random.randint(1,2))
        except:
            count += 1
            time.sleep(random.randint(1,2))
    else:
        logger.debug("关键词为…" + keyword + " 第%s页采集失败" % str(page))
        return None

async def fetch(session,data,url,entername,timeout=5):
    count = 1
    while count < 6:
        try:
            async with session.post(url=url, data=data, timeout=timeout, allow_redirects=False,headers=get_headers2()) as response:
                html = await response.text(errors='ignore')
                await asyncio.sleep(random.randint(1,2))
                if response.status in VALID_STATUS_CODE and len(html) > 100:
                    return html
                else:
                    # logger.error("正在尝试重新请求" + url)
                    count +=1
                    time.sleep(1)
        except:
            # logger.info("正在尝试重新请求" + url)
            count += 1
            time.sleep(1)
    else:
        logger.debug("企业名称为… " + entername +"企业详细信息采集失败" )
        return None



async def req_detailinfo(url,data,entername,proxy=None):
    conn = aiohttp.TCPConnector(verify_ssl=False)
    async with semaphore:
        async with aiohttp.ClientSession(connector=conn) as session:
            response = await fetch(session,data,url,entername)
            return response






