# STC Ansible

This is an *experimental* Ansible plugin to configure STC data models and execute tests. 

### Requirements

This STC Ansible module requires a recent version (>=2.5) of the Ansible client. 

This STC Ansible module can be used to remote configure an STC Lab Server. Configuration of STC-web is currently not supported.

### Installation

First, you need to install Python dependencies for the Ansible client:

```sh
pip install -r requirements.txt
```

### Running an STC Ansible Playbook

There are several example playbooks in the `playbooks` folder. 
To run all of them, just use `make play`, and it will create an STC session for each of the playbooks.

# Ansible Configuration

### Inventory

In your inventory (`inventory.ini`), declare the STC Lab Servers you want the Ansible playbook to connect to:

```ini
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

Note that `ansible_paramiko_pty` MUST be set to `no` as it will otherwise fail to connect to the STC Lab Server.

### Ansible STC Module

If you want to use the STC module outside of this direction, you will need to copy the content of the `module_utils` and `library` into the folder from which you are running your Ansible playbook.

# Let's Make an STC Ansible Playbook

### Basic STC Ansible Actions

The `stc` Ansible module makes it possible to execute one of the following five actions:

| action      | description                                                                                                                                                                                                                  |
| -------     | -------------                                                                                                                                                                                                                |
| session.    | Attach to an existing session. If the session does not exsit, a new session is created. If the session exists, the data model is first reset to the default data model.                                                      |
| load        | Loads a predefined XML data model. Note that the model must first be copied to the target STC Lab Server using the `copy` module. Check the [datamodel-loader.yaml](playbooks/datamodel-loader.yaml) playbook for reference. |
| create      | Creates a new object in the data model.                                                                                                                                                                                      |
| config      | Configures an existing object in the data model.                                                                                                                                                                             |
| perform     | Perform a command against the data model.                                                                                                                                                                                    |

### Attach to a Session

The first task of the playbook must be to attach to an STC session:

```yaml
- name: Create session
  stc: 
    action: session
    user: ansible
    name: datamodel-loader
```

### Create a Few Ports

You can then declare your own emulated device:

```yaml
- name: Create the base ports
  stc: 
    action: create
    objects: 
      - project: 
          - port: 
              location: "//(Offline)/1/1"
              name: Port 1

          - port: 
              location: "//(Offline)/2/1"
              name: Port 2
```

The STC Ansible module has a special iterator construct, which can be used to create several objects in an iterative way. For that, you only need to define the `count` property under `stc`. You can then use the keyword `${item}` as a template. The item will be replace with the values from 1 to _count_.

```yaml
- name: Create the 18 ports
  stc: 
    count: 18
    action: create
    objects: 
      - project: 
          - port: 
              location: "//(Offline)/1/${item}"
              name: "Port ${item}"
```

This will create 18 ports with the names ["Port 1".... "Port 18"], located at "//(Offline)/1/1" ... "//(Offline)/1/18".

### Create a Few Emulated Devices - Easiest Way

Once the ports are created, the next step is to create the emulated device. The easiest solution is to use the `perform` _Create Device Command_ task, which takes care of creating the interface stack:

```yaml
  name: create 20 device-blocks of 50 emulated devices each
  register: result
  stc: 
    action: perform
    command: DeviceCreate
    properties: 
      ParentList:  ref:/project
      CreateCount: 20
      DeviceCount: 50
      Port: ref:/port[Name=Port 1]
      IfStack: Ipv4If PppIf PppoeIf EthIIIf
      IfCount: '1 1 1 1'
      name: "Device ${item}"
```

Note the `ref:/port[Name=Port 1]`. This is a special construct (called a _reference_), which allows the task to reference another object in the data model. If the object does not exist, an exception is raised and the playbook stops. 

### Create a Few Emulated Devices - Extensive Way

Creating the emulated device can also be done using the `create` method, but requires configuration of all of the indiviudal properties such as the IP address and Interface stacking:

```yaml
  name: Create 20 blocks of emulated devices
  stc: 
    action: create
    under: ref:/project
    count: 20
    objects: 
    - emulateddevice: 
        AffiliatedPort: ref:/port[name=Port ${item}]
        DeviceCount: 50
        name: "Device ${item}"
        PrimaryIf: ref:./Ipv4If
        TopLevelIf: ref:./Ipv4If
        EthIIIf: 
          SourceMac: be:ef:00:00:${item}:00
        Ipv4If: 
          AddrStep: 0.0.0.2
          Address: 10.0.${item}.1
          Gateway: 192.85.1.1
          PrefixLength: 16
          stackedon: ref:./EthIIIf
```

### Reconfiguring a Data Model

Once an object is created, it is possible to update its configuration. The reference `object` of the updated object must be provided. Since there can be several objects, you usually use a named reference - `ref:/EmulatedDevice[Name= Device ${item}]` in this case:

```yaml
- name: configure the server device block
  stc: 
    action: config
    count: 20
    object: ref:/EmulatedDevice[Name= Device ${item}]
    properties:
      PppoeClientBlockConfig:
        ConnectRate: 1000
        DisconnectRate: 1000
        Authentication: CHAP_MD5
```

### Loading an XML Data Model

If declaring your own data model is too complex, you can also import an existing XML data model:

```yaml
- name: Copy the data model
  copy:
    src: asset/datamodel.xml
    dest: /tmp/datamodel.xml

- name: Load a data model
  stc:
    action: load
    datamodel: /tmp/datamodel.xml
```

Note that you must first copy the data model to the STC Lab Server before you are able to import it.

### Starting the Traffic

Starting the traffic is as simple as performing a command:

```yaml
- name: Start the traffic
  stc: 
    action: perform
    command: GeneratorStart
    properties: 
      GeneratorList: ref:/project 
```

### More Examples

Check the [playbook](playbooks) folder for more examples.

# Implementation and Design 

The STC Ansible module does not connect directly to the STC Lab Server via the STC REST API. Instead, it first `ssh` into the STC Lab Server, and then uses the REST API to connect to the BLL. 

![System Design](docs/sysdes.png)
