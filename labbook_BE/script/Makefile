.PHONY: help
help:
	@echo 'Usage:'
	@echo '  make install_shunit2   install shunit2'
	@echo '  make test              run tests'

.PHONY: install_shunit2
install_shunit2:
	cd test && \
	wget -O shunit2 https://raw.githubusercontent.com/kward/shunit2/master/shunit2

.PHONY: test
test:
	cd test && \
	test_backup.sh
