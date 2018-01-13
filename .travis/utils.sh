#!/bin/bash

ROOT_DIR=$(pwd)

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


function _generate_diagrams {
  t_dir=$(mktemp -d)
  d_dir="$ROOT_DIR/docs/diagrams"

  diagrams=$(find ${d_dir} -type f | grep '.plantuml' | sed "s|${d_dir}|/data|")
  if [ -z "${diagrams}" ]
  then
    echo "No diagrams found, skipping."
  else
    cp -r $d_dir/* $t_dir
    docker run -u $(id -u):$(id -g) --rm -v ${t_dir}:/data -it hrektts/plantuml plantuml ${diagrams}
    images=$(find ${t_dir} -type f -iname '*.png')
    mv $images "${ROOT_DIR}/docs/pages/assets/diagrams"
  fi
}


function serve_docs {
  _generate_diagrams
  mkdocs serve
}

function build_docs {
  _generate_diagrams
  mkdocs build -d out
}
