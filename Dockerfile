# Use the official Python 3.9 image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE vidura.settings

# Set the working directory
# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp
WORKDIR /opt/services/djangoapp

# Copy requirements.txt and install dependencies
COPY requirements.txt /opt/services/djangoapp
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY promptbook /opt/services/djangoapp/
COPY vidura /opt/services/djangoapp/
COPY manage.py /opt/services/djangoapp/
COPY media /opt/services/djangoapp/media

RUN python manage.py collectstatic --no-input -v 2

ENV TIME_ZONE=Asia/Shanghai \
    ENV=prod

# Expose the port the app runs on
EXPOSE 80

# Start Gunicorn to serve the Django app using ASGI
CMD ["gunicorn", "vidura.asgi:application", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80"]
