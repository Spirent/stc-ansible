
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

emulator:
	for d in ./playbooks/*; do
		python emulator.py playbooks/$d -l @rtp
	done

jenkins-regression:
	make emulator

-include makefile.local
