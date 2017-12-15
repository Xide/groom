#!/bin/bash

source .travis/utils.sh
docker_login
WDIR=$(pwd)


pushd services/server-store
container_name=server-store
docker build -t $container_name .
push_docker_image $container_name
