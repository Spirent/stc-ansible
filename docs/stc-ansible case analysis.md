# stc-ansible case analysis


## A. [STC-I-267] session create`[Finalized]`
### 1. case1 session create 

#### Description 

 	In STC-Ansible, Need to hide some of the inconsistencies among session, port and device

#### Ticket in Salesforce   
   [STC-I-267 “session create”.](https://ideas.spirent.com/ideas/STC-I-267) 

#### Yaml Samples
```
- name: Create session
    stc: 
	   action: create
	   objects:
	   - session:
	         user: ansible
	         name: session_create
	         chassis: "{{ hostvars[inventory_hostname].chassis }}"
```
###### 		--Equivalent previous yaml
	    - name: create session
	      stc: 
	          action: session
	          user: ansible
	          name: session_create
	          chassis: "{{ hostvars[inventory_hostname].chassis }}"

## B. [STC-I-265] Tag for Streamblock and EmulatedDevice
### 1.case2 tag in action create

#### Description 

 In STC Ansible, Tags & StreamBlocks names are  needs be taken care when multiple stream blocks created for scale test 

#### Ticket in Salesforce   
  [STC-I-265](https://ideas.spirent.com/ideas/STC-I-265)

#### Yaml Samples
##### 2.1 create an emulate device with one custom tag
```
- name: create an emulate device with a custom tag
  stc:
    action: create
    under: /Project
    count: 1
    objects:
    - EmulatedDevice:
        name: "BGPRouter"
        tag: "bgptag"
        AffiliatedPort: ref:/port[@name='Port1']
```
###### 		   --Equivalent previous yaml
```
  - name: create an emulate device with a custom tag
  stc:
    action: create
    under: /Project
    count: 1
    objects:
    - EmulatedDevice:
        name: "BGPRouter"
        usertag-targets: ref:/tags/tag[name=bgptag]
        AffiliatedPort: ref:/port[@name='Port1']
```


##### 2.2 create an emulate device with 2 custom tags
  ```-
- name: create an emulate device with 2 custom tags
  stc:
    action: create
    under: /Project
    count: 1
    objects:
    - EmulatedDevice:
        name: "BGPRouter"
        tag: "bgptag custom-tag-name"
        AffiliatedPort: ref:/port[@name='Port1']
  ```
###### 		   --Equivalent previous yaml
  ```
- name: create an emulate device with 2 custom tags
  stc:
    action: create
    under: /Project
    count: 1
    objects:
    - EmulatedDevice:
        name: "BGPRouter"
        usertag-targets: "ref:/tags/tag[name=bgptag] ref:/tags/tag[name=custom-tag-name]"
        AffiliatedPort: ref:/port[@name='Port1']
  ```

##### 2.3 create multiple emulate devices with one custom tag
  ```
- name: create multiple emulate devices with one custom tag
  stc:
    action: create
    under: /Project
    count: 10
    objects:
    - EmulatedDevice:
        name: "BGPRouter-$item"
        tag: "bgptag-$item"
  ```
###### 		   --Equivalent previous yaml

```
- name: create multiple emulate devices with one custom tag
  stc:
    action: create
    under: /Project
    count: 10
    objects:
    - EmulatedDevice:
        name: "BGPRouter-$item"
        usertag-targets: "ref:/tags/tag[name=bgptag-$item]"
```

##### 2.4 create bgp under multiple emulated devices by tag

###### 2.4.1 [@tag='bgptag']  or [tag='bgptag'] 
```
- name: create bgp on the devices with 'bgptag' in its tag
  stc:
    action: create
    under: /EmulatedDevice[@tag='bgptag']
    objects:
    - BgpRouterConfig:
        AsNum: 1111
        DutAsNum: 2222
        name: "BGPRouter1"
```
###### 		       --Equivalent previous yaml
tag1, tag2 are found by 'ref:/tags/tag[name=bgptag]',  tag1 and tag2's name **equal** 'bgptag'
```
   name: create bgp on the devices with the tag 'bgptag'
   stc:
     action: create
     under: /EmulatedDevice[@usertag-targets="tag1 tag2"]
     objects:
     - BgpRouterConfig:
         AsNum: 1111
         DutAsNum: 2222
         name: "BGPRouter1"
```
###### 2.4.2 [@tag\*='bgptag']  or [tag\*='bgptag'] 
```
- name: create bgp on the devices with 'bgptag' in its tag
  stc:
    action: create
    under: /EmulatedDevice[@tag*='bgptag']
    objects:
    - BgpRouterConfig:
        AsNum: 1111
        DutAsNum: 2222
        name: "BGPRouter1"
```
###### 		       --Equivalent previous yaml
tag1, tag2 are found by 'ref:/tags/tag[name*=bgptag]',  tag1 and tag2's name **contain** 'bgptag'
```
   name: create bgp on the devices with the tag 'bgptag'
   stc:
     action: create
     under: /EmulatedDevice[@usertag-targets="tag1 tag2"]
     objects:
     - BgpRouterConfig:
         AsNum: 1111
         DutAsNum: 2222
         name: "BGPRouter1"
```
###### 2.4.3 [@tag='bgptag mytag']  or [tag='bgptag mytag'] 
```
- name: create bgp on the devices with 'bgptag' and 'mytag' in its tags
  stc:
    action: create
    under: /EmulatedDevice[@tag*='bgptag']
    objects:
    - BgpRouterConfig:
        AsNum: 1111
        DutAsNum: 2222
        name: "BGPRouter1"
```
###### 		       --Equivalent previous yaml
tag1 is found by 'ref:/tags/tag[name=bgptag]',  tag1's name **equal** 'bgptag'; 
tag2 is found by 'ref:/tags/tag[name=mytag]',  tag2's name **equal** 'mytag';

```
   name: create bgp on the devices with the tag 'bgptag' and 'mytag'
   stc:
     action: create
     under: /EmulatedDevice[@usertag-targets="tag1 tag2"]
     objects:
     - BgpRouterConfig:
         AsNum: 1111
         DutAsNum: 2222
         name: "BGPRouter1"
```
### 2.case3 tag in action config
#### Description 

 In STC Ansible, Tags & StreamBlocks names are  needs be taken care when multiple stream blocks configure for scale test 

#### Ticket in Salesforce   
  [STC-I-265](https://ideas.spirent.com/ideas/STC-I-265)

#### Yaml Samples
##### 3.1 Configure one device's tag

if the device has it own tag before this config,  new tag value will overwrite the old in this device

```
 - name: Configure one device IP address and device's tag
   stc: 
    action: config
    objects: /EmulatedDevice[@Name='dev']
    properties:
        tag: "custom-tag"
        Ipv4If: 
          AddrStep: 0.0.0.1
```

###### 		   --Equivalent previous yaml
```
 - name: Configure one device IP address and device's tag
   stc: 
     action: config
     objects: /EmulatedDevice[@Name='dev']
     properties:
         usertag-targets: ref:/tags/tag[name=custom-tag]
         Ipv4If: 
           AddrStep: 0.0.0.1
         
```

##### 3.2  Configure one emulate device with 2 custom tags

if the device has it own tag before this config,  new tag value will overwrite the old in this device

```
- name: configure an emulate device with 2 custom tags
  stc: 
     action: config
     objects: /EmulatedDevice[@Name='dev']
     properties:
     	 tag: "bgptag custom-tag-name"
         Ipv4If: 
           AddrStep: 0.0.0.1
```
###### 		   --Equivalent previous yaml
```
- name: configure an emulate device with 2 custom tags
  stc: 
     action: config
     objects: /EmulatedDevice[@Name='dev']
     properties:
         usertag-targets: "ref:/tags/tag[name=bgptag] ref:/tags/tag[name=custom-tag-name]"
         Ipv4If: 
           AddrStep: 0.0.0.1
```

##### 3.3 Configure multiple devices IP address and tag

if each device has it own tag before this config,  new tag value will overwrite the old in the device

```
 - name: Configure multiple devices IP address and each device's tag
   stc: 
    action: config
    count: 20
    objects: /EmulatedDevice[@Name='dev-$item']
    properties:
        tag: "custom-tag-$item"
        Ipv4If: 
          AddrStep: 0.0.0.1
```

###### 		   --Equivalent previous yaml
```
 - name: Configure multiple devices IP address and each device's tag
   stc: 
     action: config
     count: 20
     objects: /EmulatedDevice[@Name='dev-$item']
     properties:
         usertag-targets: ref:/tags/tag[name=custom-tag-$item]
         Ipv4If: 
           AddrStep: 0.0.0.1
```
##### 3.4 configure multiple devices by its tag (each tag returns one device)
```
- name: Configure multiple devices IP address by tag (each tag returns one device)
  stc: 
    action: config
    count: 20
    objects: /EmulatedDevice[@tag='custom-tag-$item']
    properties:
        Ipv4If: 
          AddrStep: 0.0.0.2
          Address: 10.0.$item.1
```

###### 		   --Equivalent previous yaml

tag1, tag2 are found by 'ref:/tags/tag[name*=custom-tag]'

```
   name: Configure each device IP address by tag
   stc: 
     action: config
     count: 20
     objects: /EmulatedDevice[@usertag-targets="tag1 tag2"]
     properties:
         Ipv4If: 
           AddrStep: 0.0.0.2
           Address: 10.0.$item.1
```

##### 3.5 configure multiple devices by its tag (the tag returns multiple devices)

```
- name: Configure multiple devices IP address by tag (the tag returns multiple devices)
  stc: 
    action: config

    objects: /EmulatedDevice[@tag='custom-tag']
    properties:
        Ipv4If: 
          AddrStep: 0.0.0.2
          Address: 10.0.$item.1
```

* **count: 20** cannot be defined together with this case.

###### 		   --Equivalent previous yaml

tag1, tag2 are found by 'ref:/tags/tag[name*=custom-tag]'，and multiple devices are found

```
   name: Configure each device IP address by tag
   stc: 
     action: config
     objects: /EmulatedDevice[@usertag-targets="tag1 tag2"]
     properties:
         Ipv4If: 
           AddrStep: 0.0.0.2
           Address: 10.0.$item.1
```


##### 3.6 configure emulateddevice  by adding or removing one tag

```
 - name: Configure each device's tag by adding or removing one tag
   stc: 
    action: config
    count: 20
    objects: /EmulatedDevice[@Name='dev']
    properties:
        tag: "&newtag ~bgptag"
        Ipv4If: 
          AddrStep: 0.0.0.1
```

* **&** **~** can be applied as one prefix for each tag, to specify which tag to be added or removed. If the tag is not existing,  adding will create it first, removing will do nothing.

### 3.case4 tag in action perform DeviceCreate

#### Description 

 In STC Ansible, Tags & StreamBlocks names are  needs be taken care when multiple stream blocks created for scale test 

#### Ticket in Salesforce   

  [STC-I-265](https://ideas.spirent.com/ideas/STC-I-265)

#### Yaml Samples

##### 4.1 perform DeviceCreate one device with one tag

```
- name: create 20 block of 1 device with tag
  stc: 
    action: perform
    command: DeviceCreate
    properties: 
      ParentList:  ref:/project
      CreateCount: 20
      DeviceCount: 1
      Port: ref:/port[@Name='Port1']
      IfStack: Ipv4If PppIf PppoeIf EthIIIf
      IfCount: '1 1 1 1'
      name: "dev"
      tag: "mytag"
```

###### 		   --Equivalent previous yaml

```
- name: create 20 block of 1 device with tag
  stc: 
    action: perform
    command: DeviceCreate
    properties: 
      ParentList:  ref:/project
      CreateCount: 20
      DeviceCount: 1
      Port: ref:/port[@Name='Port1']
      IfStack: Ipv4If PppIf PppoeIf EthIIIf
      IfCount: '1 1 1 1'
      name: "dev"
      usertag-targets: ref:/tags/tag[name=mytag]
```

##### 4.2  perform DeviceCreate one device with 2tags

```
- name: perform DeviceCreate one device with 2 tags
  stc: 
    action: perform
    command: DeviceCreate
    properties: 
      ParentList:  ref:/project
      CreateCount: 20
      DeviceCount: 1
      Port: ref:/port[@Name='Port1']
      IfStack: Ipv4If PppIf PppoeIf EthIIIf
      IfCount: '1 1 1 1'
      name: "dev"
      tag: "mytag custom-tag-name"
```

###### 		   --Equivalent previous yaml

```
- name: perform DeviceCreate one device with 2 tags
  stc: 
    action: perform
    command: DeviceCreate
    properties: 
      ParentList:  ref:/project
      CreateCount: 20
      DeviceCount: 1
      Port: ref:/port[@Name='Port1']
      IfStack: Ipv4If PppIf PppoeIf EthIIIf
      IfCount: '1 1 1 1'
      name: "dev"
      usertag-targets: "ref:/tags/tag[name=mytag] ref:/tags/tag[name=custom-tag-name]"
```

##### 4.3 Create 50 multiple devices with tag

```
- name: create 20 block of 50 devices with tag
  stc: 
    action: perform
    command: DeviceCreate
    properties: 
      ParentList:  ref:/project
      CreateCount: 20
      DeviceCount: 50
      Port: ref:/port[@Name='Port1']
      IfStack: Ipv4If PppIf PppoeIf EthIIIf
      IfCount: '1 1 1 1'
      name: "dev-$item"
      tag: "mytag-$item"
```

###### 		   --Equivalent previous yaml

```
- name: create 20 block of 50 devices with tag
  stc: 
    action: perform
    command: DeviceCreate
    properties: 
      ParentList:  ref:/project
      CreateCount: 20
      DeviceCount: 50
      Port: ref:/port[@Name='Port1']
      IfStack: Ipv4If PppIf PppoeIf EthIIIf
      IfCount: '1 1 1 1'
      name: "dev-$item"
      usertag-targets: ref:/tags/tag[name=mytag-$item]
```
##### 4.4 perform command on multiple devices by its tag

```
- name: perform command on multiple devices by tag
  stc: 
    action: perform
    command: BgpAdvertiseRouteCommand
    properties: 
    	routelist: /EmulatedDevice[@tag*='custom-tag']
    	PrefixFilter: 4
```

###### 		   --Equivalent previous yaml

tag1, tag2 are found by 'ref:/tags/tag[name*=custom-tag]',  tag1 and tag2's name **contain** 'custom-tag'

```
- name: perform command on multiple devices by tag
  stc: 
    action: perform
    command: BgpAdvertiseRouteCommand
    properties: 
    	routelist: /EmulatedDevice[@usertag-targets="tag1 tag2"]
    	PrefixFilter: 4
```

### 4.case5 tag in action get and action delete

#### Description 

 In STC Ansible, Tags & StreamBlocks names are  needs be taken care when multiple stream blocks created for scale test 

#### Ticket in Salesforce   

  [STC-I-265](https://ideas.spirent.com/ideas/STC-I-265)

#### Yaml Samples

##### 5.1 get multiple devices by its tag

```
- name: get multiple devices attributes by its tag
  stc: 
    action: get
    objects: /EmulatedDevice[@tag*='custom-tag']
```

###### 		   --Equivalent previous yaml

tag1, tag2 are found by 'ref:/tags/tag[name*=custom-tag]',  tag1 and tag2's name **contain** 'custom-tag'

```
- name: get multiple devices attributes by its tag
  stc: 
    action: get
    objects: /EmulatedDevice[@usertag-targets="tag1 tag2"]
```

##### 5.2 delete multiple streamblocks by its tag

```
-  name: delete multiple streamblocks by tag
  stc: 
    action: delete
    objects: /Streamblock[@tag*='stream']
```

###### 		   --Equivalent previous yaml

tag1, tag2 are found by 'ref:/tags/tag[name*=stream]',  tag1 and tag2's name **contain** 'stream'

```
- name: delete multiple streamblocks IP address by tag
  stc: 
    action: delete
    objects: /Streamblock[@usertag-targets="tag1 tag2"]
```
## C. [STC-I-266] **Multiple Chassis or Single chassis connection with multiple Ports**
#### Description 

In STC Ansible, Need to pass the multiple chassis ports in the inventory file for port performance scale test

#### Ticket in Salesforce   

  [STC-I-266](https://ideas.spirent.com/ideas/STC-I-266)

#### Inventory / Yaml Samples

