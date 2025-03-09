# Build stage
FROM maven:3.5.4-jdk-8-alpine AS build

ARG DEFAULT_LOCALE
ARG MYSQL_HOST
ARG MYSQL_DATABASE
ARG MYSQL_USERNAME
ARG MYSQL_ROOT_PASSWORD
ARG SFTP_HOST
ARG SFTP_PORT
ARG SFTP_USERNAME
ARG SFTP_PASSWORD
ARG SFTP_FILES_BASE_DIR
ARG SFTP_LAYERS_BASE_DIR
ARG SFTP_OUTPUT_BASE_DIR


COPY src /app/src
COPY pom.xml /app/

RUN sed -i "s|\"DEFAULT_LOCALE\"|$DEFAULT_LOCALE|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"MYSQL_HOST\"|$MYSQL_HOST|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"MYSQL_DATABASE\"|$MYSQL_DATABASE|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"MYSQL_USERNAME\"|$MYSQL_USERNAME|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"MYSQL_PASSWORD\"|$MYSQL_ROOT_PASSWORD|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"SFTP_HOST\"|$SFTP_HOST|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"SFTP_PORT\"|$SFTP_PORT|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"SFTP_USERNAME\"|$SFTP_USERNAME|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"SFTP_PASSWORD\"|$SFTP_PASSWORD|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"SFTP_FILES_BASE_DIR\"|$SFTP_FILES_BASE_DIR|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"SFTP_LAYERS_BASE_DIR\"|$SFTP_LAYERS_BASE_DIR|g" /app/src/main/resources/application.properties && \
	sed -i "s|\"SFTP_OUTPUT_BASE_DIR\"|$SFTP_OUTPUT_BASE_DIR|g" /app/src/main/resources/application.properties

RUN mvn -f /app/pom.xml clean package

# Run stage
FROM openjdk:8-jdk-alpine
COPY --from=build /app/target/ui.backend.dck-1.0.0.jar /app/ui.backend.dck-1.0.0.jar
COPY init.sh /app/

EXPOSE 8090

ENTRYPOINT ["sh", "/app/init.sh"]
