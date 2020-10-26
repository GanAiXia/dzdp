# -*- coding: utf-8 -*-
# @Time    : 2020-07-29 09:39
# @Author  : Kingcando
# @Software: PyCharm
from flask import Flask

from App.ext import init_ext
from App.settings import envs
from App.views import init_view


def create_app(env):
    # 初始化Flask、Flask类只有一个必须指定的参数，即程序主模块或者包的名字，让flask.helpers.get_root_path函数通过传入这个名字确定程序的根目录，以便获得静态文件和模板文件的目录
    app = Flask(__name__)

    #初始化视图模块
    init_view(app)

    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 从配置获取当然运行环境配置
    app.config.from_object(envs.get(env))

    # 初始化非视图类第三方模块
    init_ext(app)

    return app
