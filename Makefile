REGISTRY_NAME=localhost
IMAGE_NAME=labbook-python
FULL_IMAGE_NAME=$(REGISTRY_NAME)/$(IMAGE_NAME)
DOCKER_COMMAND=podman
SAVE_DIR=/tmp
DEFAULT_URL_PREFIX=/sigl
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
# $(info LABBOOK_DEBUG=$(LABBOOK_DEBUG) LABBOOK_TEST_OK=$(LABBOOK_TEST_OK) LABBOOK_TEST_KO=$(LABBOOK_TEST_KO))

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

ifndef LABBOOK_DEBUG
$(error LABBOOK_DEBUG undefined)
endif

MYSQL_CMD=mysql -u $(LABBOOK_DB_USER) -p$(LABBOOK_DB_PWD) --default-character-set="UTF8"
POD_NAME=labbook
POD_NETWORK=slirp4netns:allow_host_loopback=true
CONTAINER_NAME=labbook_python
DEVRUN_HTTP=5000
DEVRUN_STORAGE?=$(shell pwd)/devrun_storage
DEVRUN_MAP_STORAGE=$(DEVRUN_STORAGE):/storage:Z
DEVRUN_FE_LOG_DIR=./labbook_FE/logs
DEVRUN_BE_LOG_DIR=./labbook_BE/logs
DEVRUN_FE_BASE_PATH=/home/apps/labbook_FE
DEVRUN_BE_BASE_PATH=/home/apps/labbook_BE
DEVRUN_GENERAL_OPTIONS=--rm --detach --pod=$(POD_NAME) --name=$(CONTAINER_NAME)
DEVRUN_ENV_OPTIONS=--tz=local --env TZ --env TERM --env LANG \
--env LABBOOK_DB_USER=$(LABBOOK_DB_USER) \
--env LABBOOK_DB_PWD=$(LABBOOK_DB_PWD) \
--env LABBOOK_DB_NAME=$(LABBOOK_DB_NAME) \
--env LABBOOK_DB_HOST=$(LABBOOK_DB_HOST) \
--env LABBOOK_DEBUG=$(LABBOOK_DEBUG) \
--env LABBOOK_TEST_OK=$(LABBOOK_TEST_OK) \
--env LABBOOK_TEST_KO=$(LABBOOK_TEST_KO) \
--env LABBOOK_USER=$(LABBOOK_USER) \
--env LABBOOK_ROOTLESS=$(LABBOOK_ROOTLESS) \
--env LABBOOK_URL_PREFIX=$(LABBOOK_URL_PREFIX) \
--env LABBOOK_POD_NAME=$(POD_NAME) \
--env LABBOOK_MEDIA_DIR=$(LABBOOK_MEDIA_DIR) \
--env LABBOOK_DUMP_COL_STATS=$(LABBOOK_DUMP_COL_STATS) \
--env LABBOOK_MAP_STORAGE=$(DEVRUN_MAP_STORAGE)
DEVRUN_VOLUME_OPTIONS=\
--volume=$(DEVRUN_MAP_STORAGE) \
--volume=./labbook_FE/app:$(DEVRUN_FE_BASE_PATH)/labbook_FE/app \
--volume=$(DEVRUN_FE_LOG_DIR):$(DEVRUN_FE_BASE_PATH)/logs \
--volume=./labbook_BE/alembic:$(DEVRUN_BE_BASE_PATH)/labbook_BE/alembic \
--volume=./labbook_BE/app:$(DEVRUN_BE_BASE_PATH)/labbook_BE/app \
--volume=./labbook_BE/script:$(DEVRUN_BE_BASE_PATH)/labbook_BE/script \
--volume=$(DEVRUN_BE_LOG_DIR):$(DEVRUN_BE_BASE_PATH)/logs

ifdef VERSION
BUILD_VERSION=$(VERSION)
else
BUILD_VERSION=$(DEFAULT_VERSION)
endif

TAG_NAME=v$(BUILD_VERSION)

URL_PREFIX=$(DEFAULT_URL_PREFIX)

ifdef LABBOOK_URL_PREFIX
DEVBUILD_URL_PREFIX=$(LABBOOK_URL_PREFIX)
else
DEVBUILD_URL_PREFIX=$(DEFAULT_URL_PREFIX)
endif

# $(info URL_PREFIX=$(URL_PREFIX) DEVBUILD_URL_PREFIX=$(DEVBUILD_URL_PREFIX))

ifndef URL_PREFIX
$(error URL_PREFIX undefined)
endif

ifndef DEVBUILD_URL_PREFIX
$(error DEVBUILD_URL_PREFIX undefined)
endif

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

.PHONY: httpdconf
httpdconf:
	mkdir -p etc/httpd/build etc/httpd/build/conf etc/httpd/build/conf.d
	sed -e "s:{{ url_prefix }}:$(URL_PREFIX):" etc/httpd/templates/conf/httpd.conf > etc/httpd/build/conf/httpd.conf
	sed -e "s:{{ url_prefix }}:$(URL_PREFIX):" etc/httpd/templates/conf.d/ssl.conf > etc/httpd/build/conf.d/ssl.conf

.PHONY: build
build: httpdconf
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
devbuild: URL_PREFIX=$(DEVBUILD_URL_PREFIX)
devbuild: httpdconf
	$(DOCKER_COMMAND) build . -t $(FULL_IMAGE_NAME):latest

.PHONY: devclean
devclean:
	$(DOCKER_COMMAND) rmi $(FULL_IMAGE_NAME):latest

.PHONY: devrun
devrun:
	mkdir -p $(DEVRUN_FE_LOG_DIR) $(DEVRUN_BE_LOG_DIR)
	mkdir -p $(DEVRUN_STORAGE)
	rsync -a ./storage/ $(DEVRUN_STORAGE)
	$(DOCKER_COMMAND) pod exists $(POD_NAME) || $(DOCKER_COMMAND) pod create --name=$(POD_NAME) --network=$(POD_NETWORK) --publish=$(DEVRUN_HTTP):80
	$(DOCKER_COMMAND) run $(DEVRUN_GENERAL_OPTIONS) $(DEVRUN_ENV_OPTIONS) $(DEVRUN_VOLUME_OPTIONS) $(FULL_IMAGE_NAME):latest

.PHONY: devstop
devstop:
	$(DOCKER_COMMAND) stop $(CONTAINER_NAME)
	$(DOCKER_COMMAND) pod stop $(POD_NAME)
	$(DOCKER_COMMAND) pod rm $(POD_NAME)
