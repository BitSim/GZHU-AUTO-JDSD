import requests
import json
import time
import os
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header
'''
下方填写key 需抓包  key在更换微信登录后会改变 具体有效期尚未可知
'''

def get_data(info_user,info_key):
    global key
    global user
    user=info_user
    key=info_key


def get_info(session,url):
    #获取个人信息 name:名字 today:今日获得积分 total:总积分
    flag = False
    info_data = {
        'route':'user_info',
        'key':key
    }
    res = session.post(url,data = info_data).json()
    info = {}
    if res['status'] == 1:
        flag = True
        info['name'] = res['re']['user_name']
        info['today'] = res['re']['per_day_credits']
        info['total'] = res['re']['credits']
    return (flag, info)


def signin(session,url):
    #签到
    signin_data = {
        'route':'signin',
        'key':key
    }
    res = session.post(url,data = signin_data).json()


def train(session,url):
    #每日一题函数, 可以直接获取每日一题题目编号, 构造编号和"1"的数组发送即可完成每日一题
    get_id_data = {
        'route':'train_list_get',
        'diff' : '0',
        'key' : key
    }
    question = session.post(url,data = get_id_data).json()
    ans = []
    for i in question['re']['question_bag']:
        ans.append([i['num'],"1"])
    train_id = question['re']['train_id']
    train_data = {
        'route':'train_finish',
        'train_id':train_id,
        'train_result' : json.dumps(ans),
        'key':key
    }
    res = session.post(url,data = train_data).json()
    if res['status'] == 1:
        return True
    else:
        return False


def read(session,url):
    #阅读函数 type从1到5 开始先发送一个开始的数据包, 结束把addtime换成91再发一次
    read_data = {
    'route' : 'classic_time',
        'addtime' : 0,
        'type':1,
        'key' : key
    }

    for i in range(1,6):
        read_data['type']=i
        read_data['addtime'] = 0
        begin = session.post(url, data = read_data)
        read_data['addtime'] = 91
        end = session.post(url, data = read_data)


def bark(flag,message = None):
    #接入bark通知 可以修改bark_url推送到自己手机(iOS only)
    bark_url = ''
    global text1,text2
    if flag:
        text1 = '{}刷分成功/'.format(time.strftime("%Y-%m-%d", time.localtime()))
        text2 = '返回信息:{}'.format(message)
    else:
        text1 = '{}刷分失败了快去看看/'.format(time.strftime("%Y-%m-%d", time.localtime()))
        text2 = '快看看'
    requests.post(bark_url+'/'+text1+text2)

def send(string,judge,to_addr):
    from_addr = 'testsend@qq.com'
    password = 'abekuewjqlmabbfe'
    # 收信方邮箱

    # 发信服务器
    smtp_server = 'smtp.qq.com'
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码x.
    msg = MIMEText(string, 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header('jdsd')  # 发送者
    msg['To'] = Header('Administrator')  # 接收者
    if judge==1:
        subject = '经典诵读运行成功'
    if judge==0:
        subject = '经典诵读运行失败'
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
    try:
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        # 建立连接--qq邮箱服务和端口号（可百度查询）
        smtpobj.connect(smtp_server, 465)
        # 登录--发送者账号和口令
        smtpobj.login(from_addr, password)
        # 发送邮件
        smtpobj.sendmail(from_addr, to_addr, msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")
    finally:
        # 关闭服务器
        smtpobj.quit()

def open_jdsd(to_addr,info_user,info_key):
    try:
        get_data(info_user,info_key)
        session = requests.session()
        headers = {
        'Host': 'jdsd.gzhu.edu.cn',
        'Accept': '*/*',
        'User-Agent': user,
        'Referer': 'https://servicewechat.com/wxb78a5743a9eed5bf/15/page-frame.html',
        'Accept-Language': 'en-us'
        }
        session.headers = headers
        url = "https://jdsd.gzhu.edu.cn/coctl_gzhu/index_wx.php"

        flag, info = get_info(session,url)
        if not flag:
            raise Exception("登录失败 请验证key")
        print("{}同学您好,您目前的积分为:{}".format(info['name'],info['total']))
        #签到+2
        signin(session,url)
        print('已完成签到')
        #进行每日一题
        for i in range(15):
            train(session,url)
        print('已完成每日一题')
        #阅读一哈
        read(session,url)
        print('已完成阅读')
        # #匹配一哈
        # vs()
        # print('已完成匹配')
        #返回
        flag, info = get_info(session,url)
        string = "今日获得:{} 总积分:{}".format(info['today'],info['total'])
        print(string)
        judge=1
        send(string,judge,to_addr)
        return string,judge
        #通知 需要填入bark_url
        #bark(1,message = string)
    except Exception as e:
        print(e)
        judge=0
        send("登录失败",judge,to_addr)
        return "登陆失败",judge
        #bark(0,message = e)