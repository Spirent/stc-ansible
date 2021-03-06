
play:
	ansible-playbook main.yaml

debug:
	ansible-playbook main.yaml -vvvv

unittest: yapf
	pytest

test: yapf
	python -m tests.playbook

yapf:
	@yapf --style '{based_on_style: google, indent_width: 4, column_limit: 120}' -i module_utils/*.py
	@yapf --style '{based_on_style: google, indent_width: 4, column_limit: 120}' -i library/*.py
	@yapf --style '{based_on_style: google, indent_width: 4, column_limit: 120}' -i tests/*.py

lint:
	pylint --rcfile=.pylint.rc module_utils/*.py

TEST_SUBDIR :=./playbooks/
TEST_LABSERVER :=@rtp

FILES := $(shell ls $(TEST_SUBDIR)*.yaml)
jenkins-regression:
	$(foreach N, $(FILES), python emulator.py -l $(TEST_LABSERVER) $(N);)

jenkins-ansible-playbook:
	ANSIBLE_VARS_PLUGINS=./tests/vars_plugins ansible-playbook main.yaml

-include makefile.local
