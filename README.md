R1: 项目初始化，学习了官网的投票应用，练习基本的命令使用

django-admin startproject mysite

python manage.py startapp polls

python manage.py runserver

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"

迁移数据库：python manage.py migrate

数据库生成：python manage.py makemigrations polls
python manage.py makemigrations noteapi

查看建表语句：python manage.py sqlmigrate polls 0001

python manage.py migrate

检查项目中的问题：python manage.py check

控制台：python manage.py shell

创建超级用户：python manage.py createsuperuser

运行测试：python manage.py test polls


R2: 添加django-ninja框架

R3
1. 增加内容md5验证，防止多地编辑产生冲突
2. 添加文章排序功能
3. 添加文章公开功能