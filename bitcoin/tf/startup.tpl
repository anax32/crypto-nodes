apt-get update
apt-get install -y --no-install-recommends \
  docker.io

docker pull ${node_repository}/${node_tag}
docker pull ${logger_repository}/${logger_tag}
