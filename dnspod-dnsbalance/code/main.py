#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Kinoko <admin@amogu.cn>
# @Date  : 2021/12/24
# @Desc  : 自动更新腾讯DNS(DNSPod)负载均衡
# @API   : https://console.cloud.tencent.com/api/explorer

import json
import random
import ssl
import time

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.dnspod.v20210323 import dnspod_client, models

# 取消全局SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 您需要设置以下参数
SecretId = "AKIDKVT**************j14sSnt"
SecretKey = "tXx84*****************qFPJxL"

DDNS = {"amogu.cn": ["ddns.01", "ddns.02", "ddns.03", "ddns.04", "ddns.05"]}  # DDNS子域名
# DNS负载均衡的子域名，需要先在DNSPod手动创建记录，更新条数由手动创建的子域名个数决定且需要与上面DDNS子域名的个数相等（A记录，免费用户2条，付费用户10条）
DNSBalance = {"amogu.cn": ["local"]}

TTL = 600  # [1-86400]默认10分钟，免费版的范围是600-86400
TIME = 300  # 检测间隔时间，单位秒


# 获取子域名解析记录
def get_record(domain, subdomain):
    cred = credential.Credential(SecretId, SecretKey)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "dnspod.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = dnspod_client.DnspodClient(cred, "", clientProfile)

    req = models.DescribeRecordListRequest()
    params = {
        "Domain": domain,
        "Subdomain": subdomain
    }
    req.from_json_string(json.dumps(params))

    resp = client.DescribeRecordList(req)
    return resp.to_json_string()


# 更新子域名解析记录
def update_record(domain, subdomain, value, record_id):
    cred = credential.Credential(SecretId, SecretKey)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "dnspod.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = dnspod_client.DnspodClient(cred, "", clientProfile)

    req = models.ModifyRecordRequest()
    params = {
        "Domain": domain,
        "SubDomain": subdomain,
        "RecordType": "A",
        "RecordLine": "默认",
        "Value": value,
        "TTL": TTL,
        "RecordId": record_id
    }
    req.from_json_string(json.dumps(params))

    resp = client.ModifyRecord(req)
    return resp.to_json_string()


# 遍历记录值(IP)
def research_record_value(domain, subdomain_list):
    ip_list = []
    # 判断是否是负载均衡域名
    for subdomain in subdomain_list:
        record_data = json.loads(get_record(domain, subdomain))["RecordList"]  # 获取记录内容
        for record in record_data:
            ip_list.append(record["Value"])
    return ip_list


# 遍历记录ID(DNS负载记录RecordID)
def research_record_id(domain, subdomain):
    id_list = []
    record_data = json.loads(get_record(domain, subdomain))["RecordList"]
    for record in record_data:
        id_list.append(record["RecordId"])
    return id_list


# MAIN
def main():
    ddns_domain = list(DDNS.keys())[0]  # DDNS的根域名
    balance_domain = list(DNSBalance.keys())[0]  # DNS负载均衡的根域名
    ddns_subdomain = DDNS[ddns_domain]  # DDNS子域名（Type: List）
    balance_subdomain = DNSBalance[balance_domain]  # DNS负载均衡子域名

    ddns_ip_list = research_record_value(ddns_domain, ddns_subdomain)  # DDNS IP记录值
    balance_ip_list = research_record_value(balance_domain, balance_subdomain)  # DNS负载均衡 IP记录值
    balance_id_list = research_record_id(balance_domain, balance_subdomain[0])  # DNS负载均衡 RecordID
    balance_num = len(ddns_subdomain)  # DNS负载均衡记录条数

    """Debug
    print(ddns_ip_list)
    print(balance_ip_list)
    print(balance_id_list)
    """

    # 开始处理
    for ip in ddns_ip_list:
        # 如果有IP不在DNS负载均衡记录值列表里则更新全部记录值
        if ip not in balance_ip_list:
            # 如果不一致则先修改DNS负载均衡子域名原先的记录值，防止IP重复无法更新记录
            for num in range(balance_num):
                # 生成随机IP地址
                random_ip = "%d.%d.%d.%d" % (
                    num + 1, random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))
                # 更新记录
                update_record(balance_domain, balance_subdomain[0], random_ip, balance_id_list[num])
            # 更新DNS负载均衡记录
            for num in range(balance_num):
                # 更新记录
                update_record(balance_domain, balance_subdomain[0], ddns_ip_list[num], balance_id_list[num])
                print("ddns_ip:", ddns_ip_list[num], "-> balance_ip:", balance_ip_list[num])
            break
        else:
            pass


if __name__ == "__main__":
    while True:
        main()
        time.sleep(TIME)
