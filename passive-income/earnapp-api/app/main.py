#!/usr/bin/python3
# coding=utf8
# @Author: Kinoko <kinoko@amogu.cn>
# @Date  : 2024/12/10
# @Desc  : EarnAPP 设备注册API
import os
import queue
import threading
import time

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 用于存储 UUID 的队列
uuid_queue = queue.Queue()


# 处理 UUID 的线程
def process_uuids():
    while True:
        try:
            # 每隔 3 秒提交队列中的 UUID
            if not uuid_queue.empty():
                uuid = uuid_queue.get()
                # 调用 API
                response = call_api(uuid)

                # 处理响应（在这里可以选择将结果存储在某个地方或打印出来）
                print(f"Result for UUID {uuid}: {response}")
                time.sleep(3)  # 每处理一个 UUID 后等待 3 秒
            else:
                time.sleep(1)  # 如果队列为空，则稍作等待以避免循环占用过多 CPU
        except Exception as e:
            print(f"Error processing UUID: {str(e)}")


# 向 API 发送请求
def call_api(uuid):
    url = f"https://earnapp.com/dashboard/api/link_device?appid=earnapp"

    # 从环境变量读取 token
    xsrf_token = os.getenv('XSRF_TOKEN')
    oauth_refresh_token = os.getenv('OAUTH_REFRESH_TOKEN')

    # 这里是请求头的字典
    headers = {
        "Xsrf-Token": xsrf_token
    }

    # 这里是 cookie 信息的字典
    cookies = {
        "xsrf-token": xsrf_token,
        "oauth-refresh-token": oauth_refresh_token
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, json={"uuid": uuid}, headers=headers, cookies=cookies)

        # 处理响应
        if response.status_code == 200:
            return response.json()  # 如果返回的结果是 JSON 格式
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@app.route('/api/get_result', methods=['POST'])
def get_request_result():
    data = request.json
    uuid = data.get('uuid')

    if not uuid:
        return jsonify({"error": "UUID is required"}), 400

    # 将 UUID 放入队列
    uuid_queue.put(uuid)
    return jsonify({"message": "UUID received, processing will start shortly."}), 202


if __name__ == "__main__":
    # 启动处理 UUID 的线程
    threading.Thread(target=process_uuids, daemon=True).start()

    # 自定义端口设置
    port = int(os.getenv("PORT", 3000))  # 默认端口为 5000
    # 启动 Flask 应用程序
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
