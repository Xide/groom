function push_docker_image {
  image="$1"
  branch=$TRAVIS_BRANCH
  commit=$TRAVIS_COMMIT
  hub_user=$DOCKER_USERNAME
  sane_branch=`echo $branch | sed "s|/|-|g" -`

  echo "Pushing docker image $1"
  if [ "$branch" == "master" ]; then
    destination="$image:stable"
  elif [ "$branch" == "develop" ]; then
    destination="$image:latest"
  else
    destination="$image-unstable:$sane_branch-$commit"
  fi
  docker tag $image $DOCKER_USERNAME/groom-$destination
  docker push $DOCKER_USERNAME/groom-$destination
}

function docker_login {
  docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
}
