FROM nginx:alpine

WORKDIR /etc/nginx
COPY ./nginx.conf ./conf.d/default.conf

EXPOSE 80

# Start Nginx in the foreground (this is already the default behavior)
ENTRYPOINT [ "nginx" ]
CMD [ "-g", "daemon off;" ]
