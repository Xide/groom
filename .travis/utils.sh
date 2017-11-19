#!/bin/bash

function push_docker_image {
  image="$1"
  branch=$TRAVIS_BRANCH
  commit=$TRAVIS_COMMIT
  hub_user=$DOCKER_USERNAME
  sane_branch=`echo $branch | sed "s|/|-|g" -`

  echo "Pushing docker image $1"
  if [ "$branch" == "master" ]; then
    destinations="$image:stable"
  elif [ "$branch" == "develop" ]; then
    destinations="$image:latest"
  else
    destinations="$image-unstable:$sane_branch-$commit,$image-unstable:$sane_branch-latest"
  fi
  IFS=',' read -ra tags <<<  "$destinations"

  for tag in "${tags[@]}"; do
    docker tag $image $DOCKER_USERNAME/groom-$tag
    docker push $DOCKER_USERNAME/groom-$tag
  done
}

function docker_login {
  docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
}
