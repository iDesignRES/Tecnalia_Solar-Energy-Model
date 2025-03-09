#!/bin/bash

echo "Building QGIS Server image..."
sleep 1
sudo docker build -t qgis:ltr -f Dockerfile .

