# first we declare our upstream server, which is our Gunicorn application
upstream vidura_server {
    # docker will automatically resolve this to the correct address
    # because we use the same name as the service: "djangoapp"
    server djangoapp:80;
}

# now we declare our main server
server {

    listen 80;
    server_name vidura.ai;

    location / {
        # everything is passed to Gunicorn
        proxy_pass http://vidura_server;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
    location /static/ {
        autoindex on;
        alias /opt/services/djangoapp/static/;
    }

    location /media/ {
        autoindex on;
        alias /opt/services/djangoapp/media/;
    }
}
