import os
from flask_script import Manager
from flask_migrate import MigrateCommand
from App import create_app

# 获取当前运行环境
env = os.environ.get('FLASK_ENV', "development")
# 初始化项目
app = create_app(env)
# manger初始化
manager = Manager(app)
# 给manager添加db命令来运行Migrate数据库迁移功能
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
