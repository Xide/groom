#!/bin/bash

source .travis/utils.sh
docker_login
WDIR=$(pwd)


cd services/server-store/command
container_name=server-store-command-amqp
docker build -t $container_name .
push_docker_image $container_name

cd services/server-store/query
container_name=server-store-query-http
docker build -t $container_name .
push_docker_image $container_name
