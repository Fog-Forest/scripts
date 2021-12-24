#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Kinoko admin@amogu.cn
# @Date  : 2021/10/22
# @Desc  : 自动更新腾讯DNS记录，DNS负载均衡
# @API   ： https://console.cloud.tencent.com/api/explorer

import json
import time

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.dnspod.v20210323 import dnspod_client, models

# 您需要设置以下参数
SecretId = "AKIDK********************14sSnt"
SecretKey = "tXx84******************FPJxL"

SubDomain = {"ddns.cn": ["ddns.01", "ddns.02", "ddns.03", "ddns.04", "ddns.05"]}  # 设置了 DDNS 的子域名
# 设置DNS负载均衡的子域名，需要先在DNSPod手动创建记录，更新条数由手动创建的子域名个数决定且需要与上面记录个数相等（A记录，免费用户2条，付费用户10条）
UpdateDomain = {"home.cn": "local"}

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
def update_record(domain, subdomain, value, recordid):
    try:
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
            "RecordId": recordid
        }
        req.from_json_string(json.dumps(params))

        resp = client.ModifyRecord(req)
        return resp.to_json_string()
    except Exception as e:
        print(e)


# MAIN
def main():
    domain1 = list(SubDomain.keys())[0]  # DDNS子域名的根域名
    domain2 = list(UpdateDomain.keys())[0]  # 需要设置DNS负载均衡子域名的根域名
    subdomain1 = SubDomain[domain1]  # DDNS子域名的记录值（Type: List）
    subdomain2 = UpdateDomain[domain2]  # 需要设置DNS负载均衡子域名的记录值
    num = 0

    # 对比记录 IP
    for record in subdomain1:
        record_ip = json.loads(get_record(domain1, record))["RecordList"][0]["Value"]
        update = json.loads(get_record(domain2, subdomain2))["RecordList"][num]
        update_ip = update["Value"]
        update_id = update["RecordId"]
        # 两个记录相同无需更新
        if record_ip == update_ip:
            pass
        else:
            update_record(domain2, subdomain2, record_ip, update_id)
            print("update ", update_ip, " to", record_ip, " success!")
        num += 1


if __name__ == "__main__":
    while True:
        main()
        time.sleep(TIME)
