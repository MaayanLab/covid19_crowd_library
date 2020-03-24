#!/usr/bin/env bash

boot() {

echo "Booting..."

echo "Writing wsgi config..."
cat | tee /app/wsgi.py << EOF
from app.app import app as application
EOF

cat | tee /app/wsgi.ini << EOF
[uwsgi]
uid = app
gid = app
master = true
processes = 5
chdir = /app
wsgi-file = /app/wsgi.py
socket = 0.0.0.0:8080
daemonize = /app/app.log
EOF

echo "Writing nginx config..."
cat | tee /app/nginx.conf << EOF
user app app;
worker_processes 1;
events {
  worker_connections 1024;
}
http {
  access_log /app/app.log;
  error_log  /app/app.log;
  gzip on;
  gzip_http_version 1.0;
  gzip_proxied      any;
  gzip_min_length   500;
  gzip_disable      "MSIE [1-6]\.";
  gzip_types        text/plain text/xml text/css
                    text/comma-separated-values
                    text/javascript
                    application/x-javascript
                    application/atom+xml;

  server {
    listen 80;

    include /etc/nginx/mime.types;
    charset utf-8;
    client_max_body_size 20M;
    sendfile on;
    keepalive_timeout 0;
    large_client_header_buffers 8 32k;

    location ${ROOT_PATH} {
      include            /etc/nginx/uwsgi_params;
      uwsgi_pass         0.0.0.0:8080;
      proxy_redirect     off;
      proxy_set_header   Host \$host;
      proxy_set_header   X-Real-IP \$remote_addr;
      proxy_set_header   X-Forwarded-For \$proxy_add_x_forwarded_for;
      proxy_set_header   X-Forwarded-Host \$server_name;
    }

    location ${ROOT_PATH}static/ {
      alias /app/static/;
    }
  }
}
EOF

echo "Starting uwsgi..."
uwsgi --ini /app/wsgi.ini || ( echo "Failed to start uwsgi..." && return 1 )

echo "Starting nginx..."
nginx -c /app/nginx.conf || ( echo "Failed to start nginx..." && return 1 )

}

die_with() {
  PID=$1
  EXIT_CODE=$(wait ${PID})
  if [ ! -z "${EXIT_CODE}" ]; then
    echo "Exited with status ${EXIT_CODE}"
  fi
  exit ${EXIT_CODE}
}

echo "Preparing log..."
if [ ! -f /app/app.log ]; then
  touch /app/app.log
fi

boot >> /app/app.log &
die_with $! &
tail -f /app/app.log
