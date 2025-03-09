FROM python:3.10.1-buster

# Declare the environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV USER="qgis"
ENV QGIS_PREFIX_PATH=/usr
ENV QGIS_SERVER_LOG_STDERR=1
ENV QGIS_SERVER_LOG_LEVEL=2
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV XDG_RUNTIME_DIR=/tmp/runtime-root

# Add the necessary packages
RUN apt-get update \
  && apt-get install --no-install-recommends --no-install-suggests --allow-unauthenticated -y \
    gnupg \
    ca-certificates \
    locales \
    apt-utils \
    curl \
    net-tools \
    dnsutils \
    iputils-ping \
    gpg \
    keyboard-configuration \
    nano \
    software-properties-common \
    supervisor \
    ssh \
    unzip \
    wget \
    xvfb

###### ADD QGIS to the system ######################################################## 

# Add QGIS-LTR repository
RUN echo "deb http://qgis.org/debian-ltr buster main" > /etc/apt/sources.list.d/qgis-latest.list

# Install QGIS
RUN wget -qO - https://qgis.org/downloads/qgis-2022.gpg.key | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import
RUN chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg
RUN apt-get update \
  && apt-get install -y \
    lxqt-core \
    build-essential \
    qgis \
    qgis-server \
    qgis-plugin-grass \
    grass \
    saga \
    libatlas-base-dev \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    libspatialindex-dev
    
# Set up SSH service to use X outside the container
RUN sed -i 's/\#X11UseLocalhost yes/X11UseLocalhost no/g' /etc/ssh/sshd_config

# Create 'qgis' user and all the necessary directories
RUN useradd -m qgis \
  && mkdir /home/qgis/api \
  && mkdir /home/qgis/database \
  && mkdir /home/qgis/dbase \
  && mkdir /home/qgis/files \
  && mkdir /home/qgis/files/tmp \
  && mkdir /home/qgis/layers \
  && mkdir /home/qgis/layers/tmp \
  && mkdir /home/qgis/output \
  && mkdir /home/qgis/projects \
  && mkdir /tmp/runtime-root

# Copy all the necessary files and directories
RUN chmod -R 777 /home/qgis/* \
  && chown qgis:qgis /home/qgis/* \
  && chmod -R 700 /tmp/runtime-root
COPY ./api /home/qgis/api

# Set the working directory
WORKDIR /home/qgis

# Install requirements (For QGIS Python version = 3.7)
RUN python3.7 -m pip install --no-cache-dir --upgrade pip \
  && python3.7 -m pip install --no-cache-dir -r /home/qgis/api/requirements.txt

# Expose the port corresponding to the REST API
EXPOSE 5010

###### Add Supervisor ##########################################################

# Add Supervisor
RUN mkdir -p /var/log/supervisor
COPY ./supervisor/ /etc/supervisor

# Run Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
