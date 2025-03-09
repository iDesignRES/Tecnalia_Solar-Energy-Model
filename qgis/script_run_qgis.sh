#!/bin/bash

xhost + &
sudo docker run --rm --name idesignres.qgis.dck \
    --privileged \
    --network idesignres_network \
    --ip 10.100.0.120 \
    --label 'traefik.enable=true' \
    --label 'traefik.http.routers.qgis.rule=Host(`idesignres.digital.tecnalia.dev`) && PathPrefix(`/api/qgis/`)' \
    --label 'traefik.http.routers.qgis.tls=true' \
    --label 'traefik.http.routers.qgis.entrypoints=websecure' \
    --label 'traefik.http.routers.qgis.tls.certresolver=myresolver' \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ./volumes/data:/root \
    -v ./volumes/dbase:/home/qgis/dbase \
    -v ./volumes/files:/home/qgis/files \
    -v ./volumes/layers:/home/qgis/layers \
    -v ./volumes/output:/home/qgis/output \
    -v ./volumes/output-tmp:/home/qgis/output-tmp \
    -e DISPLAY=unix$DISPLAY \
    qgis:ltr qgis

