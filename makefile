
play:
	ansible-playbook main.yaml

unittest: 
	pytest

test: 
	python -m tests.playbook

yapf:
	yapf --style '{based_on_style: google, indent_width: 4, column_limit: 120}' -i module_utils/*.py
	yapf --style '{based_on_style: google, indent_width: 4, column_limit: 120}' -i library/*.py
	yapf --style '{based_on_style: google, indent_width: 4, column_limit: 120}' -i tests/*.py


-include makefile.local