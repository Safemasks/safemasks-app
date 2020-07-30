#!/usr/bin/env bash
set -e


# Get the maximum upload file size for Nginx, default to 0: unlimited
USE_NGINX_MAX_UPLOAD=${NGINX_MAX_UPLOAD:-0}

# Get the number of workers for Nginx, default to 1
USE_NGINX_WORKER_PROCESSES=${NGINX_WORKER_PROCESSES:-1}

# Set the max number of connections per worker for Nginx, if requested 
# Cannot exceed worker_rlimit_nofile, see NGINX_WORKER_OPEN_FILES below
NGINX_WORKER_CONNECTIONS=${NGINX_WORKER_CONNECTIONS:-1024}

# Get the listen port for Nginx, default to 80
USE_LISTEN_PORT=${LISTEN_PORT:-80}

if [ -f /app/nginx.conf ]; then
    cp /app/nginx.conf /etc/nginx/nginx.conf
else
    content='user  nginx;\n'
    # Set the number of worker processes in Nginx
    content=$content"worker_processes ${USE_NGINX_WORKER_PROCESSES};\n"
    content=$content'error_log  /var/log/nginx/error.log warn;\n'
    content=$content'pid        /var/run/nginx.pid;\n'
    content=$content'events {\n'
    content=$content"    worker_connections ${NGINX_WORKER_CONNECTIONS};\n"
    content=$content'}\n'
    content=$content'http {\n'
    content=$content'    include       /etc/nginx/mime.types;\n'
    content=$content'    default_type  application/octet-stream;\n'
    content=$content'    server_names_hash_bucket_size   128;\n'
    content=$content'    log_format  main  '"'\$remote_addr - \$remote_user [\$time_local] \"\$request\" '\n"
    content=$content'                      '"'\$status \$body_bytes_sent \"\$http_referer\" '\n"
    content=$content'                      '"'\"\$http_user_agent\" \"\$http_x_forwarded_for\"';\n"
    content=$content'    access_log  /var/log/nginx/access.log  main;\n'
    content=$content'    sendfile        on;\n'
    content=$content'    keepalive_timeout  65;\n'
    content=$content'    include /etc/nginx/conf.d/*.conf;\n'
    content=$content'}\n'
    content=$content'daemon off;\n'                
    # Set the max number of open file descriptors for Nginx workers, if requested
    if [ -n "${NGINX_WORKER_OPEN_FILES}" ] ; then
        content=$content"worker_rlimit_nofile ${NGINX_WORKER_OPEN_FILES};\n"
    fi
    # Save generated /etc/nginx/nginx.conf
    printf "$content" > /etc/nginx/nginx.conf

    content_server='server {\n'
    content_server=$content_server"    listen ${USE_LISTEN_PORT};\n"
    content_server=$content_server"    server_name www.${DOMAIN} ${DOMAIN};\n"
    content_server=$content_server"    listen 443 ssl;\n"
    content_server=$content_server"    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;\n"
    content_server=$content_server"    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;\n"
    content_server=$content_server"    ssl_session_timeout 1440m;\n"
    content_server=$content_server"    ssl_session_cache shared:le_nginx_SSL:1m;\n"
    content_server=$content_server"    ssl_session_tickets off;\n"
    content_server=$content_server"    ssl_protocols TLSv1.2;\n"
    content_server=$content_server"    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256';\n"
    content_server=$content_server"    ssl_prefer_server_ciphers on;\n"
    content_server=$content_server"    add_header Strict-Transport-Security max-age=15768000;\n"
    content_server=$content_server"    ssl_stapling off;\n"
    content_server=$content_server"    ssl_stapling_verify on;\n"  
    content_server=$content_server'    location / {\n'
    content_server=$content_server'        proxy_redirect off;\n'
    content_server=$content_server'        proxy_pass http://0.0.0.0:90;\n'   
    content_server=$content_server'    }\n'
    content_server=$content_server'}\n'
    # Save generated server /etc/nginx/conf.d/nginx.conf
    printf "$content_server" > /etc/nginx/conf.d/nginx.conf

    # Generate Nginx config for maximum upload file size
    printf "client_max_body_size $USE_NGINX_MAX_UPLOAD;\n" > /etc/nginx/conf.d/upload.conf
fi

exec "$@"

