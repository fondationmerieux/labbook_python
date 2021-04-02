REGISTRY_NAME=localhost
IMAGE_NAME=labbook-python
FULL_IMAGE_NAME=$(REGISTRY_NAME)/$(IMAGE_NAME)
DOCKER_COMMAND=podman
SAVE_DIR=/tmp
DEFAULT_VERSION=$(shell grep "\<APP_VERSION\>" labbook_FE/default_settings.py | tr "'" '"' | sed -e 's/^.*VERSION\s\+=\s\+"//' | sed -e 's/".*$$//')

ifdef VERSION
BUILD_VERSION=$(VERSION)
else
BUILD_VERSION=$(DEFAULT_VERSION)
endif

TAG_NAME=v$(BUILD_VERSION)

ifeq (, $(shell type podman 2> /dev/null))
DOCKER_COMMAND=docker
endif

.PHONY: help
help:
	@echo 'Usage:'
	@echo '  make build [VERSION=version]       build docker image $(FULL_IMAGE_NAME):version'
	@echo '  make save [VERSION=version]        save docker image $(FULL_IMAGE_NAME):version to $(SAVE_DIR)/$(IMAGE_NAME)-VERSION.tar'
	@echo '  make clean [VERSION=version]       clean docker image $(FULL_IMAGE_NAME):version'
	@echo 'Default version value in VERSION file=$(DEFAULT_VERSION) TAG_NAME=$(TAG_NAME)'

.PHONY: build
build:
ifdef BUILD_VERSION
	git checkout $(TAG_NAME)
	$(DOCKER_COMMAND) build . -t $(FULL_IMAGE_NAME):$(BUILD_VERSION)
else
	@echo 'missing version'
endif

.PHONY: save
save:
ifdef BUILD_VERSION
	rm -f $(SAVE_DIR)/$(IMAGE_NAME)-$(BUILD_VERSION).tar
	$(DOCKER_COMMAND) save --output=$(SAVE_DIR)/$(IMAGE_NAME)-$(BUILD_VERSION).tar $(FULL_IMAGE_NAME):$(BUILD_VERSION)
	sum $(SAVE_DIR)/$(IMAGE_NAME)-$(BUILD_VERSION).tar
else
	@echo 'missing version'
endif

.PHONY: clean
clean:
ifdef BUILD_VERSION
	$(DOCKER_COMMAND) rmi $(FULL_IMAGE_NAME):$(BUILD_VERSION)
else
	$(DOCKER_COMMAND) rmi $(FULL_IMAGE_NAME)
endif
