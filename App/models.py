# -*- coding: utf-8 -*-
# @Time    : 2020-07-29 09:40
# @Author  : Kingcando
# @Software: PyCharm
from App.ext import models


# 创建数据模型
class User(models.Model):
    id = models.Column(models.Integer, primary_key=True)
    username = models.Column(models.String(16))
    userage = models.Column(models.Integer)


# 创建数据模型
class Admins(models.Model):
    id = models.Column(models.Integer, primary_key=True)
    adminname = models.Column(models.String(16))
