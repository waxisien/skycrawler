FROM nginx:1.15-alpine

WORKDIR /usr/share/nginx/html

ARG TAG
ARG DIST_ENV

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY build /usr/share/nginx/html/
