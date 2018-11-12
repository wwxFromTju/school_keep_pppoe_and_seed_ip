import os
import time
import smtplib

import requests

def check_online():
    try:
        a = requests.get(url="http://www.bilibili.com")
        if not a.headers["Connection"] == "close":
            is_login = True
            print("online")
        else:
            is_login = False
            print("offline, try to connect")
    except Exception as e:
        print(e)
        is_login = False
    return is_login


def get_local_ip():
    a = os.popen('ifconfig', 'r').read()
    b = []
    for i in a.split('\n'):
        if 'inet ad' in i.strip():
            b.append(i.strip())
    return b[-1]


def start_pppoe(sudoPassword):
    os.system('echo {}|sudo -S {}'.format(sudoPassword, 'poff -a'))
    os.system('echo {}|sudo -S {}'.format(sudoPassword, 'pon dsl-provider'))


def send_mail(body, smtp_server, stmp_send_mail, stmp_to_mails, stmp_send_mail_password):
    from_name = 'monitor' 
    cc_mail = []
    subject = u'dynamic ip'.encode('gbk')   # 以gbk编码发送，一般邮件客户端都能识别
    mail = [
        "From: %s <%s>" % (from_name, stmp_send_mail),
        "To: %s" % ','.join(stmp_to_mails),   # 转成字符串，以逗号分隔元素
        "Subject: %s" % subject,
        "Cc: %s" % ','.join(['wxwang@tju.edu.cn']),
        "",
        body]
    msg = '\n'.join(mail)
    print(msg)
    try:
        s = smtplib.SMTP()
        s.connect(smtp_server, '25')
        s.login(stmp_send_mail, stmp_send_mail_password)
        s.sendmail(stmp_send_mail, stmp_to_mails, msg)   
        s.quit()
    except smtplib.SMTPException as e:
        print("Error: %s" %e)


if __name__ == '__main__':
    while True:
        online = check_online()
        while online:
            print('hold link')
            online = check_online()
            time.sleep(10 * 60)
        sys_pass = ''
        try:
            sys_pass = os.environ['sys_pass']
        except:
            print('error sys password')
        while not online:
            start_pppoe(sys_pass)
            time.sleep(30)
            online = check_online()
        try:
            mail_auth = os.environ['mail_auth']
            password = os.environ['mail_pass']
            mail_to_auth = os.environ['mail_to_auth'].split(':')
        except:
            print('error auths')
        ip = get_local_ip()
        send_mail(ip, 'smtp.tju.edu.cn', mail_auth, mail_to_auth, password)


