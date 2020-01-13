
# STC Ansible


This is an *experimental* Ansible plugin to configure STC data-models. 

## Installation

First, you need to install the Python depencies for the Ansible client:

```
pip install -r requirements.txt
```

## Running and STC playbook

```
make play
```

# Ansible Configuration

## Inventory

In your inventory (`inventory.ini`), declare the lab servers you want the ansible playbook to connect to:

```
[labservers]
my-labserver-1 ansible_host=10.61.67.200

[labservers:vars]
ansible_connection=paramiko
ansible_host_key_checking=no
ansible_user=admin
ansible_ssh_pass=spirent
ansible_ssh_common_args=/bin/ssh
ansible_paramiko_pty=no
```

Note that `ansible_paramiko_pty` MUST be set to `no` as it will otherwise fail to connect to the Lab Server.

## Ansible STC Module

If you want to use the STC module out-side of this direction, you will need to copy the content of the `module_utils` and `library` into the folder from which you are running your ansible playbook.


# Implementation Design 

The STC ansible module does connect directly to the Lab Server via Rest API. Instead, it first `ssh` into the lab-server, and then uses the Rest API to connect to the BLL server. 


![System Design](docs/sysdes.png)