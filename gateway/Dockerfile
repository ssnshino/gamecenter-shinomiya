FROM nginx:1.28-alpine
COPY gateway/default.conf /etc/nginx/conf.d/default.conf
COPY gateway/proxy-headers.conf /etc/nginx/gamecenter-proxy-headers.conf
COPY gateway/index.html /usr/share/nginx/html/index.html
