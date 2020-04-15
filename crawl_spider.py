# -*- coding: utf-8 -*-
import re
from db_connect import RedisDbConn,DbCollect
from utils import *
from config import *
from loguru import logger
import json
import uuid
import hashlib
import asyncio




class CrawlUrl:

    def __init__(self):
        self.client = RedisDbConn()
        self.dbcollect = DbCollect()
        self.init_status = INIT_STATUS
        self.eplisturl = "https://app.gsxt.gov.cn/gsxt/cn/gov/saic/web/controller/PrimaryInfoIndexAppController/search?page="
        self.set_list = set()
        self.md5 = hashlib.md5()
        self.baseurl = "https://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-"



    def get_params(self, datalist):
        """
        构造请求参数
        :param datalist:
        :return:
        """
        for keyword in datalist:
            params = {"searchword": "%s" % keyword.decode(),
                      "conditions": {"excep_tab": "0", "ill_tab": "0", "area": "%s" % AREA, "cStatus": "0", "xzxk": "0",
                                     "xzcf": "0", "dydj": "0"}, "sourceType": "I"}
            data = json.dumps(params, ensure_ascii=False).encode("utf-8")
            for req_param in self.collect_data(data,keyword.decode()):
                yield req_param

    def rphtml(self, html):
        """
        企业名称数据处理
        :param html:
        :return:
        """
        if html:
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', html)
            return dd
        else:
            return html


    def collect_data(self,data,keyword,page=1):
        """
        基本信息采集
        :param data: 参数
        :param keyword: 关键词
        :param page: 页数，默认一页
        :return: sql params
        """
        time.sleep(random.randint(1,2))
        response = req_data(self.eplisturl, data, page,keyword)
        if response and '"status":500' not in response:
            json_value = json.loads(response)
            eplistarray = json_value["data"]["result"]["data"]
            if eplistarray:
                recordsTotal = json_value['data']['result']['recordsTotal']  # 列表记录数，判断翻页
                logger.info("关键词为^^^" + keyword + "一共" + str(recordsTotal) + "条数据......" + "目前正在采集~~~~~" + keyword + "的第" + str(page) + "页")
                for eplist in eplistarray:
                    guid = str(uuid.uuid4())
                    entName = self.rphtml(eplist['entName'])
                    pripid = eplist['pripid']
                    regNo = eplist['regNo']
                    uniscId = eplist['uniscId']
                    legelRep = eplist['legelRep']
                    entTypeCn = eplist['entTypeCn']
                    corpStatusString = eplist['corpStatusString']
                    estDate = eplist['estDate']
                    regOrg = eplist['regOrg']
                    # regCap = eplist['regCap']
                    busExceptCount = eplist['busExceptCount']
                    illCount = eplist['illCount']
                    nodeNum = eplist['nodeNum']
                    historyName = self.rphtml(eplist['historyName'])
                    entType = eplist['entType']
                    params = {'guid': guid, 'entName': entName, 'pripid': pripid,'regNo': regNo, 'uniscId': uniscId, 'legelRep': legelRep,'entTypeCn': entTypeCn,'corpStatusString': corpStatusString, 'estDate': estDate,'regOrg': regOrg, 'busExceptCount': busExceptCount,'illCount': illCount,'nodeNum': nodeNum, 'historyName': historyName,'entType': entType,'json_data':response}
                    self.md5.update(str(params).encode("utf-8"))
                    md5data = self.md5.hexdigest()
                    if md5data in self.set_list:
                        continue
                    self.set_list.add(md5data)
                    self.dbcollect.insert_basicsql("qggs_app_collectlist",params)
                    logger.info("成功采集^^^" + entName + "的基本信息...")
                    yield params


                if recordsTotal / 10 > page:
                    page += 1
                    for req_param in self.collect_data(data, keyword,page):
                        yield req_param

            self.client.set_success(keyword)
        else:
            self.client.set_failure(keyword)
            return


    async def get_detailparams(self,params):
        """
        详细页面请求参数
        :param params: 参数
        :return:
        """
        guid = eval(params)["guid"]
        pripid= eval(params)["pripid"]
        nodeNum= eval(params)["nodeNum"]
        entType = eval(params)["entType"]
        entName = eval(params)["entName"]
        # logger.info("正在采集---" + entName + "的企业信息")
        baseinfourl = self.baseurl + "primaryinfoapp-entbaseInfo-" + str(pripid) + ".html?nodeNum=" + str(nodeNum) + "&entType=" + str(entType) + "&sourceType=I"
        await self.collect_detaildata(baseinfourl,guid,params,entName)
        await asyncio.sleep(random.randint(1,2))


    async def collect_detaildata(self,baseinfourl,guid,ori_params,entername):
        """
        异步采集详细页面信息
        :param baseinfourl: 采集的url
        :param guid: 唯一编号与基本信息对应
        :param ori_params: 原始的params
        :return:
        """
        data = json.dumps({}, ensure_ascii=False).encode("utf-8")
        response = await req_detailinfo(baseinfourl, data,entername)
        await asyncio.sleep(random.randint(1,2))
        if response:
            json_value = json.loads(response)
            baseinfoarray = json_value['result']
            if baseinfoarray:
                regNo = baseinfoarray['regNo']
                uniscId = baseinfoarray['uniscId']
                regState_CN = baseinfoarray['regState_CN']
                name = baseinfoarray['name']
                industryPhy = baseinfoarray['industryPhy']
                entName = baseinfoarray['entName']
                entType_CN = baseinfoarray['entType_CN']
                regCap = baseinfoarray['regCap']
                dom = baseinfoarray['dom']
                opFrom = baseinfoarray['opFrom']
                opTo = baseinfoarray['opTo']
                opScope = baseinfoarray['opScope']
                regOrg_CN = baseinfoarray['regOrg_CN']
                regOrg = baseinfoarray['regOrg']
                estDate = baseinfoarray['estDate']
                apprDate = baseinfoarray['apprDate']
                revDate = baseinfoarray['revDate']
                regCapCur_CN = baseinfoarray['regCapCur_CN']
                baseinfojson = response
                params = {"guid":guid,"regNo":regNo,"uniscId":uniscId,"regState_CN":regState_CN,"name":name,"industryPhy":industryPhy,"entName":entName,"entType_CN":entType_CN,"regCap":regCap,"dom":dom,"opFrom":opFrom,"opTo":opTo,"opScope":opScope,"regOrg_CN":regOrg_CN,"regOrg":regOrg,"estDate":estDate,"apprDate":apprDate,"revDate":revDate,"regCapCur_CN":regCapCur_CN,"baseinfojson":baseinfojson}
                await self.dbcollect.insert_detailsql("qggs_app_baseinfo", params,ori_params)
                logger.info("成功采集^^^" + entName + "的企业详细信息...")
        else:
            self.client.set_failure(PARAMS_REDIS_DB,ori_params)





