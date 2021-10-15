#!/bin/bash

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_DEFAULT_REGION=eu-west-2

DOCKER_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
TAG=$(git describe --tags)

if [[ -z $TAG ]]
then
  exit
fi

aws --region ${AWS_DEFAULT_REGION} ecr get-login-password | docker login -u AWS --password-stdin ${DOCKER_REGISTRY}

docker tag anax32/bitcoind ${DOCKER_REGISTRY}/btc-logger/node:${TAG}
docker tag anax32/btc/logger ${DOCKER_REGISTRY}/btc-logger/logger:${TAG}

docker tag anax32/bitcoind ${DOCKER_REGISTRY}/btc-logger/node:latest
docker tag anax32/btc/logger ${DOCKER_REGISTRY}/btc-logger/logger:latest

docker push ${DOCKER_REGISTRY}/btc-logger/node:${TAG}
docker push ${DOCKER_REGISTRY}/btc-logger/logger:${TAG}

echo "${DOCKER_REGISTRY}/btc-logger/node:${TAG}"
echo "${DOCKER_REGISTRY}/btc-logger/logger:${TAG}"
