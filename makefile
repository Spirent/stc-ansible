
play:
	ansible-playbook main.yaml

test: 
	python -m tests.playbook

-include makefile.local