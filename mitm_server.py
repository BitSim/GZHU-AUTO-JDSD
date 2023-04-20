# from mitmproxy import http
# import mitmproxy
# import json
# from urllib import parse
# def request(flow: http.HTTPFlow):
#     # 获取请求URL
#     url = flow.request.url
#     # 如果请求URL符合条件（例如，包含特定的c、d、e、f请求），则打印请求详细信息
#     if "c" in url or "d" in url or "e" in url or "f" in url:
#         # print(f"Request URL: {url}")
#         # print(f"Request Headers: {flow.request.headers}")
#         # print(f"Request Content: {flow.request.content}")
#         header=f"Request Headers: {flow.request.headers}"
#         content=f"Request Content: {flow.request.content}"
#         user=header[header.index('Mozilla'):header.index("'",header.index('Mozilla'))]
#         key= content[content.index('key=')+4:-1]
#         #进行url解码，但是不会将拼接形式转换为字典形式
#         key = parse.unquote(key)
#         data={
#             'user-agent':user,
#             'key':key
#         }
#         print(data)
#         with open('data.json','w') as file_obj:
#             json.dump(data,file_obj)
#         mitmproxy.ctx.master.shutdown()

import ctypes
from ctypes import wintypes
import subprocess
import sys
import os
from db import *
path=r'{}\mitmproxy-ca-cert.cer'.format(os.getcwd())

def run_as_admin(cmd):
    # 使用ctypes.windll.shell32.IsUserAnAdmin()函数检测当前是否为管理员权限
    if ctypes.windll.shell32.IsUserAnAdmin():
        # 如果当前已经是管理员可执行该操作，直接调用subprocess.call运行命令
        return subprocess.call(cmd, shell=True)
    else:
        # 如果当前不是管理员，使用ctypes.windll.shell32.ShellExecuteW函数以管理员权限运行命令
        try:
            params = " ".join([str(i) for i in cmd])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except WindowsError:
            return -1
# init_db()
cmd = ['certutil', '-addstore','root',path]
result=run_as_admin(cmd)


