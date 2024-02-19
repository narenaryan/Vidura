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
COPY promptbook /opt/services/djangoapp/promptbook
COPY vidura /opt/services/djangoapp/vidura
COPY manage.py /opt/services/djangoapp/manage.py
COPY media /opt/services/djangoapp/media
COPY entrypoint.sh /opt/services/djangoapp/entrypoint.sh

ENV TIME_ZONE=Asia/Shanghai \
    ENV=prod

# Expose the port the app runs on
EXPOSE 80

CMD ["/opt/services/djangoapp/entrypoint.sh"]
