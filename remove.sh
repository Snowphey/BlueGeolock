#!/bin/bash

# Remove the application containers, networks, and volumes
echo "Suppression des services..."
docker compose down --volumes