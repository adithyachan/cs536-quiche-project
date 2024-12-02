# Variables
QUICHE_IMAGE_NAME := quiche-server-image
QUICHE_CONTAINER_NAME := quiche-server
QUICHE_DOCKERFILE := quiche-server/Dockerfile
QUICHE_MOUNT_SRC := $(shell pwd)/quiche-server/mount
QUICHE_MOUNT_DST := /mnt/quiche

HTTP_IMAGE_NAME := http-server-image
HTTP_CONTAINER_NAME := http-server
HTTP_DOCKERFILE := http-server/Dockerfile
QUICHE_PORT := 4433
HTTP_PORT := 8080
NETWORK_NAME := static_ip_network
QUICHE_IP := 172.18.0.3
HTTP_IP := 172.18.0.2

VENV := .venv
PYTHON := python3 

.PHONY: quiche-server
all: build-quiche run-quiche

.PHONY: build-quiche
build-quiche:
	docker build -t $(QUICHE_IMAGE_NAME) -f $(QUICHE_DOCKERFILE) .

.PHONY: run-quiche
run-quiche:
	docker network create --subnet=172.18.0.0/24 $(NETWORK_NAME) || true
	docker run -d --name $(QUICHE_CONTAINER_NAME) -p $(QUICHE_PORT):$(QUICHE_PORT) --net $(NETWORK_NAME) --ip $(QUICHE_IP) --cap-add NET_ADMIN --mount type=bind,source=$(QUICHE_MOUNT_SRC),target=$(QUICHE_MOUNT_DST),bind-propagation=rprivate $(QUICHE_IMAGE_NAME) $(BW)

.PHONY: shell-quiche
shell-quiche:
	docker exec -it $(QUICHE_CONTAINER_NAME) /bin/bash

.PHONY: stop-quiche
stop-quiche:
	docker stop $(QUICHE_CONTAINER_NAME)

.PHONY: kill-quiche
kill-quiche:
	docker rm --force $(QUICHE_CONTAINER_NAME)

.PHONY: clean-quiche
clean-quiche: kill-quiche
	docker rmi $(QUICHE_IMAGE_NAME)

.PHONY: build-http
build-http:
	docker build -t $(HTTP_IMAGE_NAME) -f $(HTTP_DOCKERFILE) .

.PHONY: run-http
run-http:
	docker run -d --name $(HTTP_CONTAINER_NAME) -p $(HTTP_PORT):$(HTTP_PORT) --net $(NETWORK_NAME) --ip $(HTTP_IP) --cap-add NET_ADMIN $(HTTP_IMAGE_NAME) $(BW)

.PHONY: shell-http
shell-http:
	docker exec -it $(HTTP_CONTAINER_NAME) /bin/bash

.PHONY: stop-http
stop-HTTP:
	docker stop $(HTTP_CONTAINER_NAME)

.PHONY: kill-http
kill-http:
	docker rm --force $(HTTP_CONTAINER_NAME)

.PHONY: clean-http
clean-http: kill-http
	docker rmi $(HTTP_IMAGE_NAME)

.PHONY: run-client
run-client:
	$(PYTHON) client/download-runner.py --bandwidth $(BW)

.PHONY: generate-download-data
generate-download-data:
	make build-http
	make build-quiche
	@for BW in 10000 100000; do \
		echo "Running tests for $$BW kbps"; \
		$(MAKE) run-http BW=$$BW; \
		$(MAKE) run-quiche BW=$$BW; \
		$(MAKE) run-client BW=$$BW; \
		$(MAKE) kill-http; \
		$(MAKE) kill-quiche; \
	done