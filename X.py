def r(min_sleep_time=3, max_sleep_time=9):
    import random
    import time
    time_random_ = random.randint(min_sleep_time * 60, max_sleep_time * 60)
    print("随机延时分钟：" + str(time_random_ / 60))
    time.sleep(time_random_)


def data_(time_str):
    from datetime import datetime
    # 解析时间字符串，并提取日期部分
    parsed_date = datetime.strptime(time_str, '%Y-%m-%d %H:%M').date()
    # 获取当前日期
    current_date = datetime.now().date()
    # 判断日期是否相同，并输出True或False
    if parsed_date == current_date:
        return True
    else:
        return False


def sendMail(mail_subject, mail_content, recv_address):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    # param mail_content 邮件内容
    # param recv_address 接收邮箱
    sender_address = '1156415978@qq.com'
    sender_pass = 'mpmxzjuwhajtbagh'
    # 怎么申请应用密码可以往下看
    message = MIMEMultipart()  # message结构体初始化
    message['From'] = sender_address  # 你自己的邮箱
    message['To'] = recv_address  # 要发送邮件的邮箱
    message['Subject'] = mail_subject
    # mail_content,发送内容,这个内容可以自定义,'plain'表示文本格式
    message.attach(MIMEText(mail_content, 'plain'))
    # 这里是smtp网站的连接,可以通过谷歌邮箱查看,步骤请看下边
    session = smtplib.SMTP('smtp.qq.com', 587)
    # 连接tls
    session.starttls()
    # 登陆邮箱
    session.login(sender_address, sender_pass)
    # message结构体内容传递给text,变量名可以自定义
    text = message.as_string()
    # 主要功能,发送邮件
    session.sendmail(sender_address, recv_address, text)
    # 打印显示发送成功
    print("send {} successfully".format(recv_address))
    # 关闭连接
    session.quit()


def get_81_code(url='http://81rc.81.cn/'):
    import requests
    from faker import Faker
    from fake_useragent import UserAgent

    # 创建一个 UserAgent 对象
    ua = UserAgent()

    fake = Faker()

    headers = {
        'Host': '81rc.81.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    cookies = {}

    html = requests.get(url, headers=headers, verify=False, cookies=cookies, proxies={"HTTP": f'{fake.ipv4_public(network=False, address_class=None)}'})
    html.encoding = html.apparent_encoding
    return html.text


def html_page(text):
    import bs4
    import re
    # lxml
    text = bs4.BeautifulSoup(text, features="lxml")
    # print(text.prettify())
    title_tags = text.find_all(attrs={"class": "left-gzdt-top"})[0]
    title_tags = title_tags.find_all("a")[0]
    # 正则
    pattern = re.compile('''href="(.*?)"''', re.S).findall(str(re.compile("""<a(.*?)</a>""", re.S).findall(str(title_tags))[0]))[0]
    return pattern


def html_work_trend(text):
    import bs4
    import re

    all__ = "军队人才网——工作动态："
    text = bs4.BeautifulSoup(text, features="lxml")
    title_tags = text.find_all(attrs={"class": "left-news"})[0].find_all("ul")[0]
    # print(title_tags)
    tags = title_tags.find_all("a")
    time = title_tags.find_all("span")
    time_test = str(re.compile('''<span>(.*?)</span>''', re.S).findall(str(time))[0])
    if data_(time_test):
        t = "有新工作动态——军队人才网"
    else:
        global Var
        Var = False
        return "无新工作动态——军队人才网", 0
    for i, j in zip(tags, time):
        HTML_text = i.text.replace("\n", "").replace("\t", "")
        URL = str(re.compile('''href="(.*?)"''', re.S).findall(str(i))[0])
        time = str(re.compile('''<span>(.*?)</span>''', re.S).findall(str(j))[0])
        all__ = all__+"\n"+HTML_text+"\t"+URL+"\t"+time
    return t, all__


import datetime

global Var
Var = True
t = get_81_code()
r()
code = get_81_code(html_page(t))
r()
B__, N__ = html_work_trend(code)

if Var:
    now = datetime.datetime.now() + datetime.timedelta(hours=8)
    B = f"{B__}  {now.strftime('%Y-%m-%d')}"
    sendMail(B, N__, '2241007756@qq.com')

