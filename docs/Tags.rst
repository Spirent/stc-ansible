Tags
====

.. contents::
   :local:
   :depth: 1

Overview
--------

Use tags to achieve scalability in large tests by organizing and viewing subsets of objects 
within a test configuration.

When creating Ports, Emulated Device or Stream blocks, the "tag" can be identified. 
Multiple tags are separated by SPACE in Ansible. Thus, SPACE is not allowed to define 
one single tag. Otherwise, it will be treated as multiple tags.


Tag Ports
---------

The example below is given by tagging each port with "Server, myPortTag-0" and "Server, myPortTag-1".

  .. code-block:: yaml

    -
      name: Create the ports
      stc:
        action: create
        count: 2
        objects:
          - project:
              - port:
                  location: ${ports[item]}
                  name: ${names[item]}
                  tag: "Server myPortTag-$item"

Tag Emulated Devices
--------------------

The example below is given by tagging each Emulated Device with "devTagDhcp, devtag-0" and "devTagDhcp, devtag-1".

  .. code-block:: yaml

    -
    name: create 2 block of 5 devices
    stc:
        action: perform
        command: DeviceCreate
        properties:
        ParentList:  ref:/project
        CreateCount: 2
        DeviceCount: 5
        Port: ref:/port[@name='Port1']
        IfStack: Ipv4If PppIf PppoeIf EthIIIf
        IfCount: '1 1 1 1'
        name: "dev-$item"
        tag: "devTagDhcp devtag-$item"


Tag Stream blocks
-----------------

The example below is given by tagging each stream block with "traffMesh, traff-0" and "traffMesh, traff-1".

  .. code-block:: yaml

    -
    name: Configure the traffic generator
    stc:
        count: 2
        action: create
        under: ref:/project
        objects:
        - StreamBlock:
            tag: "traffMesh traff-$item"
            EnableStreamOnlyGeneration: true
            TrafficPattern: MESH
            SrcBinding-targets: ref:/EmulatedDevice[@name='dev-$item']/Ipv4If
            DstBinding-targets: ref:/EmulatedDevice[@name!='dev-$item']/Ipv4If
            AffiliationStreamBlockLoadProfile:
            Load: 100