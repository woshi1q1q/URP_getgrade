#coding=utf-8

import requests,re

def get_grade():
    s=requests.session()
    posturl='http://202.197.144.243:8083/loginAction.do'
    zih=input('输入学号:')
    mm=input('输入密码:')
    data={'zjh':zih,'mm':mm}
    #登录教务系统
    r=s.post(posturl,data)
    #进入成绩网址
    grade='http://202.197.144.243:8083/bxqcjcxAction.do'
    g=s.get(grade).text
    #使用正则获取成绩部分
    re_pattag=r'align="center">\s*(.*?)\s*<'
    g=re.findall(re_pattag,g)
    #打印成绩
    print('-------------成绩详情-------------')
    for i in range(0,len(g),7):
        print('%s:%s'%(g[i:i+7][2],g[i:i+7][-1]))

get_grade()
