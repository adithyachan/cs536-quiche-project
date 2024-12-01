# Variables
QUICHE_IMAGE_NAME := quiche-server-image
QUICHE_CONTAINER_NAME := quiche-server
QUICHE_DOCKERFILE := quiche-server/Dockerfile
QUICHE_MOUNT_SRC := $(shell pwd)/quiche-server/mount
QUICHE_MOUNT_DST := /mnt/quiche
PORT := 4433

PYTHON := python3 

.PHONY: quiche-server
all: build-quiche run-quiche

.PHONY: build-quiche
build-quiche:
	docker build -t $(QUICHE_IMAGE_NAME) -f $(QUICHE_DOCKERFILE) .

.PHONY: run-quiche
run-quiche:
	docker run -d --name $(QUICHE_CONTAINER_NAME) -p $(PORT):$(PORT) --cap-add NET_ADMIN --mount type=bind,source=$(QUICHE_MOUNT_SRC),target=$(QUICHE_MOUNT_DST),bind-propagation=rprivate $(QUICHE_IMAGE_NAME) $(BW)

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

.PHONY: run-client
run-client:
	$(PYTHON) client/client-runner.py

