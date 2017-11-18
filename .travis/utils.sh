function push_docker_image {
  image="$1"
  branch=$TRAVIS_BRANCH
  commit=$TRAVIS_COMMIT
  echo "Pushing docker image $1"
  if [ "$branch" == "master" ]; then
    destination="$image:stable"
  elif [ "$branch" == "develop"]; then
    destination="$image:latest"
  else
    destination="$image-unstable:$branch-$commit"
  fi
  docker tag $image Xide/groom-$destination
  docker push Xide/groom-$destination
}
