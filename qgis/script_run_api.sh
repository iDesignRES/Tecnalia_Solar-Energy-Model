#!/bin/bash

sudo docker exec -it idesignres.qgis.dck /bin/bash -c 'rm /home/qgis/layers/ES21*.*';
sudo docker exec -it idesignres.qgis.dck python3.7 api/api.py
