#!/bin/bash

# Remove the application containers, networks, and volumes
echo "Suppression des services..."
docker compose down --volumes

# Construction et démarrage
echo "Construction des images Docker..."
docker compose build

echo "Démarrage des services..."
docker compose up -d