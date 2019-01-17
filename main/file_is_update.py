# _*_encoding:utf-8_*_

# 调度文件
# 使用HTTP请求头的IMS（If-Modified-Since）标签
import file_operation as fileOp
import configure_file as conf
import sys
import logging  # 引入logging模块
import requests
import hashlib
from requests.exceptions import ReadTimeout
from requests.exceptions import HTTPError
import datetime
import ssl
import os

os.system("pause")
# logging.basicConfig函数对日志的输出格式及方式做相关配置
# logging.basicConfig(level=logging.WARNING, format=conf.logFormat)
# 取消验证
ssl._create_default_https_context = ssl._create_unverified_context

# 读取sqllite网址信息
recode_json = fileOp.read_sqlite(conf.sqlite_path, conf.can_check_sql)
if recode_json:  # 如果字典不为空
    siteList = list(recode_json.keys())
else:
    print "dict from sqlite is None"
    sys.exit()

'''
# 读取json文件信息并读入内存
recode_json = fileOp.read_file_to_json(conf.json_path)
for i in range(len(siteList)):
    if siteList[i] not in recode_json:
        recode_json[siteList[i]] = {}
'''
print "the check is running -----------------------"
# 请求头设置
headers = {"User-Agent": conf.user_agent,
           "Accept": conf.accept}
while True:
    for i in range(len(siteList)):
        # 将lastModified, eTag加入到headers里
        if "last_modified" in recode_json[siteList[i]] and recode_json[siteList[i]]["last_modified"]:
            headers["If-Modified-Since"] = recode_json[siteList[i]]["last_modified"]
        if "eTag" in recode_json[siteList[i]] and recode_json[siteList[i]]["eTag"]:
            headers["If-None-Match"] = recode_json[siteList[i]]["eTag"]
        # print headers
        response = None
        try:
            # print str(i) + ":"
            resp = requests.get(siteList[i], headers=headers, timeout=5)
            # print u"开始爬取第" + str(i) + u"个：" + siteList[i] + u"状态码," + str(resp.status_code)
            if resp.status_code == 200:
                html_text = resp.text
                html_text_hash = hashlib.md5(html_text.encode(encoding="utf-8")).hexdigest()
                if recode_json[siteList[i]]:
                    if "hash_text" in recode_json[siteList[i]]:
                        if recode_json[siteList[i]]["hash_text"] != html_text_hash:
                            # print recode_json[siteList[i]]
                            # print recode_json[siteList[i]]["hash_text"]
                            # print html_text_hash
                            # fileOp.update_sqlite_dynamic(conf.sqlite_path, siteList[i])
                            print u"********注意：已经更新：" + siteList[i] + u",发现更新时间：" + str(datetime.datetime.now())
                            print u"********网址名称：" + recode_json[siteList[i]]["url_name"]
                            # print "can not check," + siteList[i]
                            # print recode_json[siteList[i]]["hash_text"]
                            # print html_text_hash
                        # else:
                            # print u"hash 无更新：" + siteList[i]
                dict_flag = {}
                # 将更新的lastModified和eTag加入到内存里
                if "Last-Modified" in resp.headers:
                    dict_flag["last_modified"] = resp.headers["Last-Modified"]
                else:
                    dict_flag["last_modified"] = ""
                    # 二维数组这样赋值错误
                    # recode_json[siteList[i]]["lastModified"] = resp.headers["Last-Modified"]
                    # print "Last-Modified," + siteList[i]
                if "ETag" in resp.headers:
                    dict_flag["eTag"] = resp.headers["ETag"]
                else:
                    dict_flag["eTag"] = ""
                    #recode_json[siteList[i]]["eTag"] = resp.headers["ETag"]
                # 如果两个Flag都没有，则下载整个页面并计算杂凑值
                #if not recode_json[siteList[i]]:

                dict_flag["hash_text"] = html_text_hash
                # 更新sqlite  last_modified,eTag,hash_text
                fileOp.update_sqlite_context(conf.sqlite_path,
                                             siteList[i],
                                             last_modified=dict_flag["last_modified"],
                                             etag=dict_flag["eTag"],
                                             hash_text=dict_flag["hash_text"])
                # 更新内存
                recode_json[siteList[i]] = dict_flag
            # if "Expires" in resp.headers:
                # print "Expires," + siteList[i]
            elif resp.status_code == 304:
                # print "304," + siteList[i]
                pass
            else:
                print "can not visit," + siteList[i]
        except HTTPError, e:  # 处理http错误
            print "httpError," + siteList[i]
            continue
        except ReadTimeout, e:
            print "timeoutError," + siteList[i]
            continue
        except Exception, e:
            print "exceptionError," + siteList[i] + "," + str(e)
            continue
    print "have pass a turn"

# 将hash字典记录到json文件里
# fileOp.write_json_to_filepath(conf.json_path, recode_json)

