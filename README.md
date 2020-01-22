# STC Ansible

This is an *experimental* [Ansible](https://www.ansible.com/) plugin to configure Spirent Test Center data models and execute tests. 

[![CircleCI](https://circleci.com/gh/Spirent/stc-ansible.svg?style=svg)](https://circleci.com/gh/Spirent/stc-ansible)

### Requirements

This STC Ansible module requires a recent version (>=2.5) of the Ansible client. 

This STC Ansible module can be used to remote configure an STC Lab Server. 

Configuration of STC-web is currently not supported.

### Installation

First, you need to install Python dependencies for the Ansible client:

```sh
pip install -r requirements.txt
```

### Running an STC Ansible Playbook

There are several example playbooks in the `playbooks` folder. 
To run all of them, just use `make play`, and it will create an STC session for each of the playbooks.
(You can also use `make debug` to run ansible with extra verbose output).


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

The `stc` Ansible module makes it possible to execute one of the following 8 actions:

| action      | description                                                                                                                                                                                                                  |
| -------     | -------------                                                                                                                                                                                                                |
| session.    | Attach to an existing session. If the session does not exsit, a new session is created. If the session exists, the data model is first reset to the default data model.                                                      |
| load        | Loads a predefined XML data model. Note that the model must first be copied to the target STC Lab Server using the `copy` module. Check the [datamodel-loader.yaml](playbooks/datamodel-loader.yaml) playbook for reference. |
| create      | Creates a new object in the data model.                                                                                                                                                                                      |
| config      | Configures an existing object in the data model.                                                                                                                                                                             |
| perform     | Perform a command against the data model.                                                                                                                                                                                    |
| delete      | Deletes an object in the data model.                                                                                                                                                                                         |
| get         | Returns the value of a given attribute of one or more objects - this can be used for instance to check results                                                                                                   |
| wait        | Waits for one of several object attribute to become a specific value (eg wait for the attritube `BlockState` of the PPPoE object `PppoeClientBlockConfig` to become `CONNECTING` )                                        |
| download     | Download files such as _bll.log_, _bll.session.log_, etc...                              |

### Attach to a Session

The first task of the playbook must be to attach to an STC session:

```yaml
- name: Create session
  stc: 
    action: session
    user: ansible
    name: datamodel-loader
```

There are two optional parameters: `kill_existing` and `reset_existing`: If the session already exists on the server, it will respectively be first killed, or reset (using the _ResetConfig_ command)

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


### Attaching to real chassis

In the previous task, the chassis where defined as offline. It is howerver possible to add a list of chassis to the inventory,
and reference them in the tasks. 

The first step is to declare the chassis in the inventory. For instance, this will add the two chassis `10.61.67.128` and `10.61.67.131` to the playbook.

```ini
[labservers]
my-labserver-1 ansible_host=10.61.67.200 chassis = "10.61.67.128 10.61.67.131"
```

Then, when creating the session, specify the chassis property:

```yaml
- name: Create a session with predefined chassis
  stc: 
    action: session
    user: ansible
    name: basic_device
    chassis: "{{ hostvars[groups['labservers'][0]].chassis }}"
```

The `{{ hostvars[groups['labservers'][0]].chassis }}` is used to reference to the chassis defined in the inventory. Alternatively, you can directly specify the chassis IP in the task, such `chassis: "10.61.67.128 10.61.67.131"`

Once the chassis are defined, the `session` task will automatically connect to them when the session is created. Then, in order to reference the chassis IP address from the task, one can use the keywork `${chassis[0]}` ... `${chassis[1]}` or even `${chassis[item]}`.

```yaml
- name: Create the base ports
  register: result
  stc: 
    action: create
    objects: 
      - project: 
          - port: 
              location: "//${chassis[0]}/1/1"
              name: Port1

          - port: 
              location: "//${chassis[1]}/1/1"
              name: Port2
```

Voila, last step is to add a task to attach to the ports:

```yaml
-
  name: Take the ports online
  stc: 
    action: perform
    command: AttachPorts
    properties:
      RevokeOwner: true
      PortList: ref:/port
```

Notice the reference `ref:/port`: It refers to all the port handles.


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


### Waiting for a condition

When using learned addresses, such as for PPPoE, it can be usefull to wait for all the clients to have their IP address learned. This can be done using the `wait` command. For instance, this will wait for emulated device _PPPoE Client_ to have all of it's IP resolved: 

```yaml
- name: Wait for the clients to be bound
  stc: 
    action: wait
    object: ref:/EmulatedDevice[Name=PPPoE Client]/PppoeClientBlockConfig
    until: BlockState=CONNECTED
```


### Getting and displaying results

Last, once the test is finished, it is possible to get some results from the properties of the result object defined in the data model. The following example get the values of the `PppoeServerBlockResults` object, and prints it.

```yaml
- name: Get the binding results
  register: results
  stc:
    action: get
    object: ref:/EmulatedDevice[Name=PPPoE Server]/PppoeServerBlockConfig/PppoeServerBlockResults

- debug:
    var: result
```


### Debugging

Debugging can be difficult when using Ansible. To make it easier to troubleshoot your playbook, you can use the STC ansible emulator. For example:

```
./emulator.py -labserver lab-serverIP-address you-playbook.yaml
```




### More Examples

Check the [playbook](playbooks) folder for more examples.

# Implementation and Design 

The STC Ansible module does not connect directly to the STC Lab Server via the STC REST API. Instead, it first `ssh` into the STC Lab Server, and then uses the REST API to connect to the BLL. 

![System Design](docs/sysdes.png)
