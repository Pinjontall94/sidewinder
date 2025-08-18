DOCKER_USERNAME := pinjontall94
IMAGE_NAME := sidewinder
GIT_HASH := $(shell git rev-parse --short HEAD)

build:
	docker build --tag $(DOCKER_USERNAME)/$(IMAGE_NAME):$(GIT_HASH) .

push:
	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):$(GIT_HASH)

release:
	docker pull $(DOCKER_USERNAME)/$(IMAGE_NAME):$(GIT_HASH)
	docker image tag $(DOCKER_USERNAME)/$(IMAGE_NAME):$(GIT_HASH) $(DOCKER_USERNAME)/$(IMAGE_NAME):latest
	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):latest
