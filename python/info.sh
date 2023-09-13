#!/bin/bash

# Display containers
echo "---- Containers ----"
docker ps -a

# Display images
echo "---- Images ----"
docker images

# Display volumes
echo "---- Volumes ----"
docker volume ls

# Display networks
echo "---- Networks ----"
docker network ls
