FROM httpd:2.4.33

ARG BACKEND_URL

COPY htdocs /usr/local/apache2/htdocs
RUN sed -i "s|\"BACKEND_URL\"|$BACKEND_URL|g" /usr/local/apache2/htdocs/config/config.json

EXPOSE 80
