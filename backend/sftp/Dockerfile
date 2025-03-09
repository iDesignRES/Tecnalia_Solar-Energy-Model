FROM alpine

# Parameters from the Dockerfile
ARG SFTP_ROOT_DIRECTORY
ARG SFTP_GROUPNAME
ARG SFTP_USERNAME
ARG SFTP_PASSWORD
ARG SFTP_UID_GID

# Install OpenSSH Server
RUN apk add --no-cache openssh
COPY ./sshd_config /etc/ssh/

# Create de default directories
RUN mkdir /idesignres \
  && mkdir /idesignres/dbase \
  && chmod 777 /idesignres/dbase \
  && mkdir /idesignres/files \
  && chmod 777 /idesignres/files \
  && mkdir /idesignres/layers \
  && chmod 777 /idesignres/layers \
  && mkdir /idesignres/resources \
  && chmod 777 /idesignres/resources \
  && mkdir /idesignres/output \
  && chmod 777 /idesignres/output \
  && mkdir /idesignres/output-tmp \
  && chmod 777 /idesignres/output-tmp

# Create the output directories for the different users
RUN mkdir /idesignres/output/admin \
  && chmod 777 /idesignres/output/admin \
  && mkdir /idesignres/output/operator \
  && chmod 777 /idesignres/output/operator \
  && mkdir /idesignres/output-tmp/admin \
  && chmod 777 /idesignres/output-tmp/admin \
  && mkdir /idesignres/output-tmp/operator \
  && chmod 777 /idesignres/output-tmp/operator

# Copy the dbase files
COPY dbase/* /idesignres/dbase/

# Copy the files
COPY files/* /idesignres/files/

# Copy the layers
COPY layers/* /idesignres/layers/

# Copy the resources
COPY resources/* /idesignres/resources/

# Create the Group
RUN addgroup --gid $SFTP_UID_GID $SFTP_GROUPNAME

# Create the users
RUN adduser -h $SFTP_ROOT_DIRECTORY -H -u $SFTP_UID_GID \
    -G $SFTP_GROUPNAME $SFTP_USERNAME;\
    echo $SFTP_USERNAME:$SFTP_PASSWORD | chpasswd

COPY ./entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh

EXPOSE 22

CMD ["/usr/bin/entrypoint.sh"]
