#!/bin/bash

# 应用数据库迁移
echo "Applying database migrations..."
python manage.py migrate --noinput

# 创建超级用户
echo "Creating superuser..."
python manage.py createsuperuserfromenv

# 收集静态文件
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# 启动Gunicorn服务器
echo "Starting Gunicorn server..."
# Start Gunicorn to serve the Django app using ASGI
exec gunicorn vidura.asgi:application -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80
