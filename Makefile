REGISTRY_NAME=localhost
IMAGE_NAME=labbook-python
FULL_IMAGE_NAME=$(REGISTRY_NAME)/$(IMAGE_NAME)
DOCKER_COMMAND=podman
SAVE_DIR=/tmp
SQLDUMP_FILENAME=etc/sql/demo_dump.sql

DEFAULT_VERSION=$(shell grep "\<APP_VERSION\>" labbook_FE/default_settings.py | tr "'" '"' | sed -e 's/^.*VERSION\s\+=\s\+"//' | sed -e 's/".*$$//')
DB_USER=$(shell grep "\<DB_USER\>" labbook_BE/default_settings.py | tr "'" '"' | sed -e 's/^.*USER\s\+=\s\+"//' | sed -e 's/".*$$//')
DB_PWD=$(shell grep "\<DB_PWD\>" labbook_BE/default_settings.py | tr "'" '"' | sed -e 's/^.*PWD\s\+=\s\+"//' | sed -e 's/".*$$//')
DB_NAME=$(shell grep "\<DB_NAME\>" labbook_BE/default_settings.py | tr "'" '"' | sed -e 's/^.*NAME\s\+=\s\+"//' | sed -e 's/".*$$//')
# $(info DEFAULT_VERSION=$(DEFAULT_VERSION) DB_USER=$(DB_USER) DB_PWD=$(DB_PWD) DB_NAME=$(DB_NAME))

MYSQL_CMD=mysql -u $(DB_USER) -p$(DB_PWD) --default-character-set="UTF8"
POD_NAME=labbook
CONTAINER_NAME=labbook_python
DEVRUN_HTTP=5000
DEVRUN_STORAGE?=./devrun_storage
DEVRUN_GENERAL_OPTIONS=--rm --detach --pod=$(POD_NAME) --name=$(CONTAINER_NAME)
DEVRUN_ENV_OPTIONS=--tz=local --env TZ --env TERM --env LANG --env SERVER_EXT=$(shell hostname)
# TODO add volume option(s) to mount local application code into the container
DEVRUN_VOLUME_OPTIONS=--volume=/var/lib/mysql:/var/lib/mysql:Z --volume=$(DEVRUN_STORAGE):/storage:Z

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
	@echo '  make build [VERSION=version]       build image $(FULL_IMAGE_NAME):version from $(TAG_NAME) tag'
	@echo '  make save [VERSION=version]        save image $(FULL_IMAGE_NAME):version to $(SAVE_DIR)/$(IMAGE_NAME)-version.tar'
	@echo '  make clean [VERSION=version]       remove image $(FULL_IMAGE_NAME):version'
	@echo 'Default version value in VERSION file=$(DEFAULT_VERSION) TAG_NAME=$(TAG_NAME)'
	@echo ''
	@echo 'For developers:'
	@echo '  make dbtest        test connection to MySQL with username=$(DB_USER) password=$(DB_PWD)'
	@echo '  make dbinit        initialize $(DB_NAME) database from $(SQLDUMP_FILENAME)'
	@echo '  make devbuild      build image $(FULL_IMAGE_NAME):latest from working directory'
	@echo '  make devclean      remove image $(FULL_IMAGE_NAME):latest'
	@echo '  make devrun        run container connected to local MySQL database $(DB_NAME)'

.PHONY: build
build:
ifdef BUILD_VERSION
	git checkout $(TAG_NAME)
	$(DOCKER_COMMAND) build . -t $(FULL_IMAGE_NAME):$(BUILD_VERSION)
	git checkout master
else
	@echo 'missing version'
endif

.PHONY: save
save:
ifdef BUILD_VERSION
	rm -f $(SAVE_DIR)/$(IMAGE_NAME)-$(BUILD_VERSION).tar $(SAVE_DIR)/$(IMAGE_NAME)-$(BUILD_VERSION).tar.xz
	$(DOCKER_COMMAND) save --output=$(SAVE_DIR)/$(IMAGE_NAME)-$(BUILD_VERSION).tar $(FULL_IMAGE_NAME):$(BUILD_VERSION)
	xz --keep $(SAVE_DIR)/$(IMAGE_NAME)-$(BUILD_VERSION).tar
	(cd $(SAVE_DIR) && \
	 md5sum $(IMAGE_NAME)-$(BUILD_VERSION).tar > $(IMAGE_NAME)-$(BUILD_VERSION).tar.md5sum && \
	 md5sum $(IMAGE_NAME)-$(BUILD_VERSION).tar.xz > $(IMAGE_NAME)-$(BUILD_VERSION).tar.xz.md5sum)
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

.PHONY: dbtest
dbtest:
	echo "show databases" | $(MYSQL_CMD)

.PHONY: dbinit
dbinit:
	echo "drop database if exists $(DB_NAME)" | $(MYSQL_CMD)
	echo "create database $(DB_NAME)" | $(MYSQL_CMD)
	echo "source $(SQLDUMP_FILENAME)" | $(MYSQL_CMD) -D $(DB_NAME)

.PHONY: devbuild
devbuild:
	$(DOCKER_COMMAND) build . -t $(FULL_IMAGE_NAME):latest

.PHONY: devclean
devclean:
	$(DOCKER_COMMAND) rmi $(FULL_IMAGE_NAME):latest

.PHONY: devrun
devrun:
	mkdir -p $(DEVRUN_STORAGE)
	rsync -a ./storage/ $(DEVRUN_STORAGE)
	$(DOCKER_COMMAND) pod exists $(POD_NAME) || $(DOCKER_COMMAND) pod create $(POD_NAME) --publish=$(DEVRUN_HTTP):80
	$(DOCKER_COMMAND) run $(DEVRUN_GENERAL_OPTIONS) $(DEVRUN_ENV_OPTIONS) $(DEVRUN_VOLUME_OPTIONS) $(FULL_IMAGE_NAME):latest
