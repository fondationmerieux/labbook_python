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

VERSION_NAME=v$(BUILD_VERSION)

ifeq (, $(shell type podman 2> /dev/null))
DOCKER_COMMAND=docker
endif

.PHONY: help
help:
	@echo 'Usage:'
	@echo '  make build [VERSION=version]       build docker image $(FULL_IMAGE_NAME):VERSION_NAME'
	@echo '  make save [VERSION=version]        save docker image $(FULL_IMAGE_NAME):version to $(SAVE_DIR)/$(IMAGE_NAME)_VERSION_NAME.tar'
	@echo 'Default version value in VERSION file=$(DEFAULT_VERSION) VERSION_NAME=$(VERSION_NAME)'

.PHONY: build
build:
ifdef BUILD_VERSION
	git checkout $(VERSION_NAME)
	$(DOCKER_COMMAND) build . -t $(FULL_IMAGE_NAME):$(VERSION_NAME)
else
	@echo 'missing version'
endif

.PHONY: save
save:
ifdef BUILD_VERSION
	$(DOCKER_COMMAND) save --output=$(SAVE_DIR)/$(IMAGE_NAME)-$(BUILD_VERSION).tar $(FULL_IMAGE_NAME):$(BUILD_VERSION)
else
	@echo 'missing version'
endif
