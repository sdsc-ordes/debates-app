# Use the official Nginx image based on Alpine
FROM nginx:alpine

# Set the working directory for Nginx
WORKDIR /etc/nginx

# Copy the custom Nginx configuration file to the appropriate directory
COPY ./nginx.conf ./conf.d/default.conf

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start Nginx in the foreground (this is already the default behavior)
ENTRYPOINT [ "nginx" ]
CMD [ "-g", "daemon off;" ]

