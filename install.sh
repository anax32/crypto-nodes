# initialisation script
# run as root/sudo

apt-get update && \
apt-get install -yq \
  tmux \
  docker-compose \
  git \
  python3-pip

python3 -m pip install tmuxp
