# -*- coding: utf-8 -*-
# @Time    : 2020-07-29 09:41
# @Author  : Kingcando
# @Software: PyCharm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

# 懒加载SQLAlchemy模块
models = SQLAlchemy()
# 懒加载数据迁移模块
migrate = Migrate()


def init_ext(app):
    # 初始化数据模块
    models.init_app(app)
    # 初始化数据迁移模块
    migrate.init_app(app, models)
    DebugToolbarExtension(app)
