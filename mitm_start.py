from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy import http
import mitmproxy
from urllib import parse
from winproxy import ProxySetting
from db import *
class Addon:
    def request(self,flow: http.HTTPFlow):
        url = flow.request.url
        
        if url=='https://jdsd.gzhu.edu.cn/coctl_gzhu/index_wx.php':
            # 如果请求URL符合条件（例如，包含特定的c、d、e、f请求），则打印请求详细信息
            if "c" in url or "d" in url or "e" in url or "f" in url:
                # print(f"Request URL: {url}")
                # print(f"Request Headers: {flow.request.headers}")
                # print(f"Request Content: {flow.request.content}")
                try:
                    header=f"Request Headers: {flow.request.headers}"
                    content=f"Request Content: {flow.request.content}"
                    user=header[header.index('Mozilla'):header.index("'",header.index('Mozilla'))]
                    key= content[content.index('key=')+4:-1]
                    #进行url解码，但是不会将拼接形式转换为字典形式
                    key = parse.unquote(key)
                    print(key)
                    user_key_insert(user,key)
                    mitmproxy.ctx.master.shutdown()
                except:
                    print(1)
p = ProxySetting()

def set_proxy():
    """设置系统代理"""
    p.enable = True
    p.server = '127.0.0.1:11205'
    p.registry_write()


def close_proxy():
    """关闭系统代理"""
    p.enable = False
    p.registry_write()

def start_mitm():
    myaddon=Addon()
    opts = options.Options(listen_host='0.0.0.0', listen_port=11205)
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(myaddon)
    m.run() 