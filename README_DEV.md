# 修改表结构的方法

1. 修改Model定义
2. 运行 `python manage.py makemigrations`，这一步会生成一个迁移文件，位于 `promptbook/migrations/` 目录下
3. 运行 `python manage.py migrate`，这一步会在数据库中更新表结构