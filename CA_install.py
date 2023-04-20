import ctypes, sys, os
import subprocess
import requests
import ssl
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

import time
def admin_exe() :
    user_home = os.path.expanduser('~')
    filepath=r'{}\.mitmproxy\mitmproxy-ca-cert.cer'.format(user_home)
    print(filepath)
    if is_admin():
        print("admin_exe函数内，以管理员权限运行")
        print(1)
        subprocess.call(["certutil", "-addstore","root",filepath])
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return 0

def CA_down():
    user_home = os.path.expanduser('~')
    filepath=r'{}\.mitmproxy\mitmproxy-ca-cert.cer'.format(user_home)
    max_wait_time = 60  # 最大等待时间为60秒
    waited_time = 0  # 已等待时间

    while not os.path.exists(filepath) and waited_time < max_wait_time:
        time.sleep(1)
        waited_time += 1

    if os.path.exists(filepath):
        print('文件已存在')
        return filepath
    else:
        print('等待超时，文件未找到')


#判断证书是否已经安装
def mitm_install():
    context = ssl.create_default_context()

    certs = context.get_ca_certs()
    for cert in certs:
        if(cert['subject'][0][0][1]=='mitmproxy'):
            return 1
    return 0