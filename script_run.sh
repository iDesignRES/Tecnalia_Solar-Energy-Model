#!/bin/bash

# Run Backend + UI + Reverse proxy
gnome-terminal --title="Backend + UI + Proxy" --tab -e "sudo docker compose -f docker-compose.yaml up -d"
sleep 2

# Run QGIS Server
gnome-terminal --title="QGIS Server" --tab -e "bash qgis/script_run_qgis.sh &"
sleep 4

# Run the REST API
gnome-terminal --title="REST API" --tab -e "bash qgis/script_run_api.sh &"

