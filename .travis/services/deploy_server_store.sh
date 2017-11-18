#!/bin/bash

source ../utils.sh
WDIR=$(pwd)

cd services/server-store/command
container_name=server-store-command-amqp
docker build -t $container_name .
push_docker_image $container_name
