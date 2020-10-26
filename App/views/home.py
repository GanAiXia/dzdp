# -*- coding: utf-8 -*-
# @Time    : 2020-07-29 09:42
# @Author  : Kingcando
# @Software: PyCharm
import random
import re

import parsel
from flask import Blueprint, render_template, request
from pip._vendor import requests

from App.models import models, User

# 设置蓝图
home = Blueprint('home', __name__)


# 主页
@home.route('/')
@home.route('/index')
def index():
    return render_template("index.html")


@home.route('/test', methods=['GET', 'POST'])
def test():
    dph = '请填写店铺号'
    return render_template("test.html", dph=dph)


@home.route('/dzdp', methods=['GET', 'POST'])
def dzdp():
    dianpu = request.form.get('wangzhi')
    # qianzhui = request.form.get('qianzhui')
    dpurl = ''
    if dianpu is not None:
        # 店铺地址拼接完成
        dpurl = 'http://www.dianping.com/shop/' + dianpu + '/review_all'
        # print(dpurl)
        # headers
        headers = {
            "Cookie": "fspop=test; cy=1; cye=shanghai; _lxsdk_cuid=1751d2b07bcc8-02ea334c58ad33-333376b-1fa400-1751d2b07bcc8; _lxsdk=1751d2b07bcc8-02ea334c58ad33-333376b-1fa400-1751d2b07bcc8; _hc.v=2865efd4-0890-7e92-7cd5-33d758992332.1602512161; s_ViewType=10; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1602512161,1602798437; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1602799097; expand=yes; _lxsdk_s=1752e3b3c6d-7f1-29e-b05%7C%7C327",
            "Host": "www.dianping.com",
            "Referer": dpurl,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"

        }

        response = requests.get(dpurl, headers=headers)
        # print(response.text)
        # 保存页面
        # print(response)
        with open('dzdpjiami.html', mode='w', encoding='utf-8') as f:
            f.write(response.text)
        css_url = re.findall('<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.*?)">', response.text)
        #
        css_url = 'http:' + css_url[0]
        # print(css_url)
        css_response = requests.get(css_url)
        with open('cssres.css', mode='w', encoding='utf-8') as f:
            f.write(css_response.text)
        # print(css_response.text)

        svg_url = re.findall(r'svgmtsi\[class\^="rp"\].*?background-image: url\((.*?)\);', css_response.text)
        svg_url = 'http:' + svg_url[0]
        # print(svg_url)
        svg_response = requests.get(svg_url)
        with open('svgysb.svg', mode='w', encoding='utf-8') as f:
            f.write(svg_response.text)
        # print(svg_response.text)

        with open('svgysb.svg', mode='r', encoding='utf-8') as f:
            svg_html = f.read()

        sel = parsel.Selector(svg_html)

        texts = sel.css('text')
        lines = []
        # print(texts)
        for text in texts:
            # print(text.css("text::text").get())
            # print(text.css("text::attr(y)").get())
            lines.append([int(text.css("text::attr(y)").get()), text.css("text::text").get()])

        # print(lines)
        if lines:
            msg = '获取数据成功'

    return render_template('jiemi.html', msg=msg)


@home.route('/jiemi')
def jiemi():
    with open('svgysb.svg', mode='r', encoding='utf-8') as f:
        svg_html = f.read()

    sel = parsel.Selector(svg_html)

    texts = sel.css('text')
    lines = []
    for text in texts:
        # print(text.css("text::text").get())
        # print(text.css("text::attr(y)").get())
        lines.append([int(text.css("text::attr(y)").get()), text.css("text::text").get()])

    with open('cssres.css', mode='r', encoding='utf') as f:
        css_text = f.read()
    class_map = re.findall('\.(rp\w+)\{background:-(\d+)\.0px -(\d+)\.0px;\}', css_text)
    # print(class_map)
    class_map = [(cls_name, int(x), int(y)) for cls_name, x, y in class_map]
    d_map = {}

    for one_char in class_map:
        try:
            cls_name, x, y = one_char
            # print(one_char)
            for line in lines:
                # print(line)
                if line[0] < y:
                    pass
                else:
                    index = int(x / 14)
                    char = line[1][index]
                    # print('___')
                    # print(cls_name, char)
                    d_map[cls_name] = char

                    break
        except Exception as e:
            print(e)

    print(d_map)

    with open('dzdpjiami.html', mode='r', encoding='utf-8') as f:
        html = f.read()

    for key, value in d_map.items():
        html = html.replace('<svgmtsi class="' + key + '"></svgmtsi>', value)

    with open('dzdpjiemi.html', mode='w', encoding='utf-8') as f:
        f.write(html)
    return '解密成功'


@home.route('/createdb')
def create_db():
    models.create_all()

    return 'Create Table Success!'


# 添加数据
@home.route('/adduser')
def add_user():
    user = User()
    user.username = "kingcando%d" % (random.randint(1, 1000))
    user.userage = random.randint(1, 100)
    models.session.add(user)
    models.session.commit()

    return 'Insert Success!'


# 删库
@home.route('/dropdb')
def drop_db():
    models.drop_all()

    return 'Drop Tables Success!'
