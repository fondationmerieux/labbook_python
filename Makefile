REGISTRY_NAME=localhost
IMAGE_NAME=labbook-python
FULL_IMAGE_NAME=$(REGISTRY_NAME)/$(IMAGE_NAME)
DOCKER_COMMAND=podman
SAVE_DIR=/tmp
SQLDUMP_FILENAME=etc/sql/demo_dump.sql
CONFIG_DIR=$(HOME)/.config
CONFIG_FILENAME=labbook.conf
CONFIG_PATH1=$(CONFIG_DIR)/$(CONFIG_FILENAME)
CONFIG_PATH2=$(HOME)/$(CONFIG_FILENAME)

DEFAULT_VERSION=$(shell grep "\<APP_VERSION\>" labbook_FE/default_settings.py | tr "'" '"' | sed -e 's/^.*VERSION\s\+=\s\+"//' | sed -e 's/".*$$//')

ifneq ("$(wildcard $(CONFIG_PATH1))","")
include $(CONFIG_PATH1)
else ifneq ("$(wildcard $(CONFIG_PATH2))","")
include $(CONFIG_PATH2)
endif

# $(info DEFAULT_VERSION=$(DEFAULT_VERSION) LABBOOK_DB_USER=$(LABBOOK_DB_USER) LABBOOK_DB_PWD=$(LABBOOK_DB_PWD) LABBOOK_DB_NAME=$(LABBOOK_DB_NAME))

ifndef LABBOOK_DB_USER
$(error LABBOOK_DB_USER undefined)
endif

ifndef LABBOOK_DB_PWD
$(error LABBOOK_DB_PWD undefined)
endif

ifndef LABBOOK_DB_NAME
$(error LABBOOK_DB_NAME undefined)
endif

ifndef LABBOOK_DB_HOST
$(error LABBOOK_DB_HOST undefined)
endif

MYSQL_CMD=mysql -u $(LABBOOK_DB_USER) -p$(LABBOOK_DB_PWD) --default-character-set="UTF8"
POD_NAME=labbook
CONTAINER_NAME=labbook_python
DEVRUN_HTTP=5000
DEVRUN_STORAGE?=./devrun_storage
DEVRUN_FE_BASE_PATH=/home/apps/labbook_FE
DEVRUN_BE_BASE_PATH=/home/apps/labbook_BE
DEVRUN_FE_DIRS=alembic app script
DEVRUN_GENERAL_OPTIONS=--rm --detach --pod=$(POD_NAME) --name=$(CONTAINER_NAME)
DEVRUN_ENV_OPTIONS=--tz=local --env TZ --env TERM --env LANG \
--env LABBOOK_DB_USER=$(LABBOOK_DB_USER) \
--env LABBOOK_DB_PWD=$(LABBOOK_DB_PWD) \
--env LABBOOK_DB_NAME=$(LABBOOK_DB_NAME) \
--env LABBOOK_DB_HOST=$(LABBOOK_DB_HOST)
DEVRUN_VOLUME_OPTIONS=\
--volume=$(DEVRUN_STORAGE):/storage:Z \
--volume=./labbook_FE/app:$(DEVRUN_FE_BASE_PATH)/labbook_FE/app \
--volume=./labbook_BE/alembic:$(DEVRUN_BE_BASE_PATH)/labbook_BE/alembic \
--volume=./labbook_BE/app:$(DEVRUN_BE_BASE_PATH)/labbook_BE/app \
--volume=./labbook_BE/script:$(DEVRUN_BE_BASE_PATH)/labbook_BE/script

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
	@echo ''
	@echo 'When shipping an image:'
	@echo '  make build [VERSION=version]       build image $(FULL_IMAGE_NAME):version from $(TAG_NAME) tag'
	@echo '  make save [VERSION=version]        save image $(FULL_IMAGE_NAME):version to $(SAVE_DIR)/$(IMAGE_NAME)-version.tar,'
	@echo '                                     compress tar to tar.xz and compute md5sums for them'                           
	@echo '  make clean [VERSION=version]       remove image $(FULL_IMAGE_NAME):version'
	@echo 'Default version value in VERSION file=$(DEFAULT_VERSION) TAG_NAME=$(TAG_NAME)'
	@echo ''
	@echo 'For developers:'
	@echo '  make dbtest        test connection to MySQL with username=$(LABBOOK_DB_USER) password=$(LABBOOK_DB_PWD)'
	@echo '  make dbinit        initialize $(LABBOOK_DB_NAME) database from $(SQLDUMP_FILENAME)'
	@echo '  make devbuild      build image $(FULL_IMAGE_NAME):latest from working directory'
	@echo '  make devclean      remove image $(FULL_IMAGE_NAME):latest'
	@echo '  make devrun        run the application access from http://localhost:$(DEVRUN_HTTP)/sigl'
	@echo '  make devstop       stop the application'

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
	echo "drop database if exists $(LABBOOK_DB_NAME)" | $(MYSQL_CMD)
	echo "create database $(LABBOOK_DB_NAME)" | $(MYSQL_CMD)
	echo "source $(SQLDUMP_FILENAME)" | $(MYSQL_CMD) -D $(LABBOOK_DB_NAME)

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
	$(DOCKER_COMMAND) pod exists $(POD_NAME) || $(DOCKER_COMMAND) pod create --name=$(POD_NAME) --publish=$(DEVRUN_HTTP):80
	$(DOCKER_COMMAND) run $(DEVRUN_GENERAL_OPTIONS) $(DEVRUN_ENV_OPTIONS) $(DEVRUN_VOLUME_OPTIONS) $(FULL_IMAGE_NAME):latest

.PHONY: devstop
devstop:
	$(DOCKER_COMMAND) stop $(CONTAINER_NAME)
	$(DOCKER_COMMAND) pod stop $(POD_NAME)
	$(DOCKER_COMMAND) pod rm $(POD_NAME)
