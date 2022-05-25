Emulated Device
===============

.. contents::
   :local:
   :depth: 1

Overview
--------

Using `STC Ansible` module, you can create and configure multiple emulated devices distributed throughout 
the ports in a test.

To create an emulated device, use `EmulatedDevice` object under the project object affiliated with any available
ports.

You can configure all the characteristics of an emulated device as well as the interface stack objects during 
the creation of emulated device. Same can also be reconfigured/modify later.

An emulated device can be designated as a router, host, client, server by confiugring specific protocols in it
or it can simply use as a traffic-only device.

Once the emulated device creation and configuration is done, you can configure the Streamblock/traffic generator
between the devices by setting the source and destination with device object references. Please refer `StreamBlock <../docs/StreamBlock.rst>`_ section.

Then, you can verify the traffic statistics (transmitted and received packets) between the 
emulated devices by starting the traffic.

Create Emulated Device
----------------------

Purpose
~~~~~~~

Creates emulated device object(s) in the Spirent Test Center(stc) datamodel under the project object
affiliated with any created port object(s).
During the object creation, requires to configure interface stacking and individual properties like ip address,
gateway, devicecount, name etc.
The name of the emulated device object will be used as a reference in order to reconfigure/modify
any of it's properties later.

In `STC Ansible` module, an emulated device can be created in 2 ways.
  1. Using the `perform` method and `DeviceCreate` command. It is an esiest way which takes care of 
     creating the interface stack.
  2. Using the `create` method. It is an extensive way which requires configuration of all of the 
     indiviudal properties such as the IP address and Interface stacking.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   
   -
      name: create emulated device using `perform`
      stc: 
         action: perform  :mandatory:`M`
         command: DeviceCreate  :mandatory:`M`
         properties: 
            ParentList:  ref:/project   :mandatory:`M`
            CreateCount: <number of deviceblocks>
            DeviceCount: <number of devices>
            Port: <port object path>   :mandatory:`M`
            IfStack: <list of the interface objects>  :mandatory:`M`
            IfCount: <interface count in list>  :mandatory:`M`
            name: <device name>
   
For the properties details of first method (creating emulateddevice using `perform`), please refer
`DeviceCreate Command Reference Document <http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/DeviceCreateCommand.htm>`_.

.. parsed-literal::
   
   -
      name: create emulated device using `create`
      stc: 
         action: create  :mandatory:`M`
         under: <project object reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <emulated device object name>  :mandatory:`M`
                AffiliatedPort: <port object reference> :mandatory:`M`
                PrimaryIf: <reference to primary interface> :mandatory:`M`
                TopLevelIf: <reference to top-level interface> :mandatory:`M`
                <emulated device attribute1: value1>
                <emulated device attribute2: value2>
                .
                .

Parameters
~~~~~~~~~~

.. raw:: html
    
   <!DOCTYPE html>
   <html>
   <head>
   <style>
      table {
        border-collapse: collapse;
        width: 100%;
      }

   td, th {
     border: 1px solid #dddddd;
     text-align: left;
     padding: 8px;
   }

   tr:nth-child(even) {
     background-color: #dddddd;
   }
   </style>
   </head>
   <body>

   <table>
     <tr>
       <th style="text-align: center">Parameter</th>
       <th style="text-align: center">Value Type</th>
       <th style="text-align: center">Description</th>
     </tr>
     <tr>
       <td>action</td>
       <td>string</td>
       <td>
           <div>Specifies the action for the given task. Here, it is <code>create</code>.</div>
           <div><b>Required:</b> Yes</div>
       </td>
     </tr>
     <tr>
       <td>under</td>
       <td>xpath</td>
       <td>
            <div>A project under which an emulateddevice is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>under: /project</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='../docs/Port.rst'>Port section</a></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. Port must already exist.</div>
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of emulated devices to be created.</div>
          <div>Count value above 1, creates several emulated device objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create emulateddevice, use <code>EmulatedDevice</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/EmulatedDevice.htm'> EmulatedDevice object reference guide</a><div>
          <div> Following are some direct links to specific interface objects. Same are also available in 'EmulatedDevice object reference guide' link given above.</div>
          <div>For EthIIIf properties <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/EthIIIf.htm'> EthIIIf object reference page
          </a></div>
          <div>For VlanIf properties <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/VlanIf.htm'> VlanIf object reference page 
          </a><div>
          <div>For Ipv4If properties <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ipv4If.htm'> Ipv4If object reference page 
          </a><div>
          <div>For Ipv6If properties <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ipv6If.htm'> Ipv6If object reference page 
          </a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

  1. Sample YAML code to create IPv4 emulated devices:
  
  .. code-block:: yaml

    -
    name: create one IPv4 emulated device using 'perform'
    stc: 
        action: perform
        command: DeviceCreate
        properties: 
        ParentList:  ref:/project
        CreateCount: 1
        DeviceCount: 1
        Port: ref:/port[@Name='port1']
        IfStack: Ipv4If EthIIIf
        IfCount: 1 1
        name: "device1"

    -
      name: create one IPv4 emulated device using 'create'
      stc: 
        action: create
        under: ref:/project
        count: 1
        objects: 
          - emulateddevice:
             AffiliatedPort: ref:/port[@name='Port1']
             DeviceCount: 1
             name: "Device1"
             PrimaryIf: ref:./Ipv4If
             TopLevelIf: ref:./Ipv4If
             EthIIIf:
               SourceMac: 00:10:94:00:00:01
             Ipv4If:
               Address: "192.85.1.2"
               Gateway: "192.85.1.1"
               PrefixLength: 24
               stackedon: ref:./EthIIIf

  2. Sample YAML code to create IPv4 emulated devices with single VLAN:
  
  .. code-block:: yaml


    -
      name: create one IPv4 emulated device with single vlan
      stc: 
        action: create
        under: ref:/project
        count: 1
        objects: 
          - emulateddevice:
            AffiliatedPort: ref:/port[@name='Port1']
            DeviceCount: 1
            name: "Device1"
            PrimaryIf: ref:./Ipv4If
            TopLevelIf: ref:./Ipv4If
            EthIIIf:
              SourceMac: 00:10:94:00:00:01
            VlanIf:
              VlanId: "101"
              StackedOnEndpoint-targets: ref:./EthIIIf
            Ipv4If:
              Address: "192.85.1.2"
              Gateway: "192.85.1.1"
              PrefixLength: 24
              StackedOnEndpoint-targets: ref:./VlanIf
              TopLevelIfSource: ref:/EmulatedDevice[@Name="Device1"]
              PrimaryIfSource: ref:/EmulatedDevice[@Name="Device1"]

    -
    name: create one IPv4 emulated device with vlan using 'perform'
    stc: 
        action: perform
        command: DeviceCreate
        properties: 
           ParentList:  ref:/project
           CreateCount: 1
           DeviceCount: 1
           Port: ref:/port[@Name='port1']
           IfStack: Ipv4If VlanIf EthIIIf
           IfCount: 1 1 1
           name: "device1"

  3. Sample YAML code to create IPv4 emulated devices with double VLAN:
  
  .. code-block:: yaml

    -
    name: create one IPv4 emulated device with dual vlan using 'perform'
    stc:
        action: perform
        command: DeviceCreate
        properties:
        ParentList:  ref:/project
        CreateCount: 1
        DeviceCount: 1
        Port: ref:/port[@Name='Port1']
        IfStack: Ipv4If VlanIf VlanIf EthIIIf
        IfCount: '1 1 1 1'
        name: "ipv4_dual_vlan_2"


    -
    name: create one IPv4 emulated device with dual vlan using 'create'
    stc:
        action: create
        under: ref:/project
        count: 1
        objects:
        - emulateddevice:
            AffiliatedPort: ref:/port[@name='Port1']
            DeviceCount: 1
            name: "ipv4_dual_vlan_1"
            PrimaryIf: ref:./Ipv4If
            TopLevelIf: ref:./Ipv4If
            EthIIIf:
                SourceMac: 00:10:96:00:00:01
            VlanIf:
                VlanId: 100
            Ipv4If:
                AddrStep: 0.0.0.1
                Address: 192.168.1.2
                Gateway: 192.168.1.1
                TopLevelIfSource: ref:/EmulatedDevice[@Name='ipv4_dual_vlan_1']
                PrimaryIfSource: ref:/EmulatedDevice[@Name='ipv4_dual_vlan_1']
    
    -
    name: create VlanIf under ipv4_dual_vlan
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name='ipv4_dual_vlan_1']
        count: 1
        objects:
        - VlanIf:
            VlanId: 100
    
    -
    name: config Ipv4If for ipv4_dual_vlan
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_dual_vlan_1']/Ipv4If
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_dual_vlan_1']/VlanIf[1]
    
    -
    name: config VlanIf 2 - ipv4_dual_vlan
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_dual_vlan_1']/VlanIf[1]
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_dual_vlan_1']/VlanIf[0]
    
    -
    name: config VlanIf 1 - ipv4_dual_vlan
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_dual_vlan_1']/VlanIf[0]
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_dual_vlan_1']/EthIIIf


  4. Sample YAML code to create multiple IPv4 emulated devices:
  
  .. code-block:: yaml


    -
      name: create 50 IPv4 emulated devices
      stc: 
        action: create
        under: ref:/project
        count: 50
        objects: 
          - emulateddevice:
            AffiliatedPort: ref:/port[@name='Port1']
            DeviceCount: 1
            name: "Device$item"
            PrimaryIf: ref:./Ipv4If
            TopLevelIf: ref:./Ipv4If
            EthIIIf:
              SourceMac: 00:10:94:00:00:$item
            VlanIf:
              VlanId: "10$item"
              StackedOnEndpoint-targets: ref:./EthIIIf
            Ipv4If:
              Address: "192.85.1.${item+3}"
              Gateway: "192.85.1.1"
              PrefixLength: 24
              StackedOnEndpoint-targets: ref:./VlanIf
              TopLevelIfSource: ref:/EmulatedDevice[@Name="Device$item"]
              PrimaryIfSource: ref:/EmulatedDevice[@Name="Device$item"]

  5. Sample YAML code to create IPv6 emulated device:
  
  .. code-block:: yaml

    -
      name: create one IPv6 emulated device using 'create' method
      stc: 
        action: create
        under: ref:/project
        count: 1
        objects: 
          - emulateddevice:
              AffiliatedPort: ref:/port[@name='Port1']
              DeviceCount: 1
              name: "ipv6_device_1"
              PrimaryIf: ref:./Ipv6If
              TopLevelIf: ref:./Ipv6If
              EthIIIf:
                SourceMac: 00:10:94:00:00:01
              Ipv6If:
                Address: "2000::2"
                Gateway: "2000::1"
                PrefixLength: 64

    -
      name: Create linklocal ipv6if under ipv6_device_1
      stc:
        action: create
        under: ref:/EmulatedDevice[@Name='ipv6_device_1']
        count: 1
        objects:
          - Ipv6If:
              AddrStep: ::1
              Address: fe80::1
              PrimaryIfSource: ref:/EmulatedDevice[@Name='ipv6_device_1']
              TopLevelIfSource: ref:/EmulatedDevice[@Name='ipv6_device_1']

    -
      name: config EthIIIf stack relation
      stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv6_device_1']/EthIIIf
          properties:
            stackedonendpoint-Sources: ref:/EmulatedDevice[@Name='ipv6_device_1']/Ipv6If

    ######################################################################################
    -
    name: create one IPv6 emulated device using 'perform'
    stc:
        action: perform
        command: DeviceCreate
        properties:
        ParentList:  ref:/project
        CreateCount: 1
        DeviceCount: 1
        Port: ref:/port[@Name='Port2']
        IfStack: Ipv6If EthIIIf
        IfCount: '1 1'
        name: "ipv6_device_2"
    
    -
    name: Config ipv6if address
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv6_device_2']/Ipv6If
        properties:
           Address: 2002::3
           Gateway: 2002::1
    
    -
    name: Create ipv6if
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name="ipv6_device_2"]
        count: 1
        objects:
        - Ipv6If:
            AddrStep: ::1
            Address: fe80::1
            PrimaryIfSource: ref:/EmulatedDevice[@Name="ipv6_device_2"]
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv6_device_2"]
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv6_device_2"]/EthIIIf

  6. Sample YAML code to create IPv6 emulated device with single VLAN:
  
  .. code-block:: yaml

    -
      name: Create one IPv6 emulated device with single vlan using 'create' method
      stc:
        action: create
        under: ref:/project
        count: 1
        objects:
          - emulateddevice:
              AffiliatedPort: ref:/port[@name='Port1']
              DeviceCount: 1
              name: "ipv6_single_vlan_1"
              PrimaryIf: ref:./Ipv6If
              TopLevelIf: ref:./Ipv6If
              EthIIIf:
                SourceMac: 00:10:96:00:00:01
              VlanIf:
                VlanId: 100
                StackedOnEndpoint-targets: ref:./EthIIIf
              Ipv6If:
                AddrStep: ::1
                Address: 2001::2
                Gateway: 2001::1
                StackedOnEndpoint-targets: ref:./VlanIf
                TopLevelIfSource: ref:/EmulatedDevice[@Name='ipv6_single_vlan_1']
                PrimaryIfSource: ref:/EmulatedDevice[@Name='ipv6_single_vlan_1']

    -
      name: Create ipv6if under device 1
      stc:
        action: create
        under: ref:/EmulatedDevice[@Name='ipv6_single_vlan_1']
        count: 1
        objects:
           - Ipv6If:
                  AddrStep: ::1
                  Address: fe80::2
                  PrimaryIfSource: ref:/EmulatedDevice[@Name='ipv6_single_vlan_1']
                  TopLevelIfSource: ref:/EmulatedDevice[@Name='ipv6_single_vlan_1']
                  StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv6_single_vlan_1']/VlanIf

    ###########################################################################################
    -
    name: Create one IPv6 emulated device with single vlan using 'perform' method
    stc:
        action: perform
        command: DeviceCreate
        properties:
        ParentList:  ref:/project
        CreateCount: 1
        DeviceCount: 1
        Port: ref:/port[@Name='Port2']
        IfStack: Ipv6If VlanIf EthIIIf
        IfCount: '1 1 1'
        name: "ipv6_single_vlan_2"
    
    -
    name: Create ipv6if
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name="ipv6_single_vlan_2"]
        count: 1
        objects:
        - Ipv6If:
            AddrStep: ::1
            Address: fe80::1
            PrimaryIfSource: ref:/EmulatedDevice[@Name="ipv6_single_vlan_2"]
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv6_single_vlan_2"]
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv6_single_vlan_2"]/VlanIf

  7. Sample YAML code to create IPv6 emulated device with double VLAN:
  
  .. code-block:: yaml

    -
    name: Create one IPv6 emulated device with double vlan using 'create' method
    stc:
        action: create
        under: ref:/project
        count: 1
        objects:
        - emulateddevice:
            AffiliatedPort: ref:/port[@name='Port1']
            DeviceCount: 1
            name: "ipv6_dual_vlan_1"
            PrimaryIf: ref:./Ipv6If
            TopLevelIf: ref:./Ipv6If
            EthIIIf:
               SourceMac: be:ef:00:00:00:00
            VlanIf:
               VlanId: 100
            Ipv6If:
               AddrStep: ::1
               Address: 2001::2
               Gateway: 2001::1
    
    -
    name: Create linklocal ipv6if
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]
        count: 1
        objects:
        - Ipv6If:
            AddrStep: ::1
            Address: fe80::1
            PrimaryIfSource: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]
    
    -
    name: create second VlanIf under emulated device
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]
        count: 1
        objects:
        - VlanIf:
            VlanId: 100
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]/VlanIf[0]
    
    -
    name: config ipv6if stack relation
    stc:
        action: config
        count: 1
        objects: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]/Ipv6If[0]
        properties:
          StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]/VlanIf[1]
    
    -
    name: config VlanIf stack relation
    stc:
        action: config
        count: 1
        objects: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]/VlanIf[0]
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]/EthIIIf
    
    -
    name: config linklocal Ipv6If stack relation
    stc:
        action: config
        count: 1
        objects: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]/Ipv6If[1]
        properties:
           StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_1"]/VlanIf[1]

    #########################################################################################
    -
    name: Create one IPv6 emulated device with double vlan using 'perform' method
    stc:
        action: perform
        command: DeviceCreate
        properties:
        ParentList:  ref:/project
        CreateCount: 1
        DeviceCount: 1
        Port: ref:/port[@Name='Port2']
        IfStack: Ipv6If VlanIf VlanIf EthIIIf
        IfCount: '1 1 1 1'
        name: "ipv6_dual_vlan_2"

    -
    name: Create ipv6if
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_2"]
        count: 1
        objects:
        - Ipv6If:
            AddrStep: ::1
            Address: fe80::3
            PrimaryIfSource: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_2"]
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_2"]
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv6_dual_vlan_2"]/VlanIf[0]

  8. Sample YAML code to create dualstack(IPv4IPv6) emulated device:
  
  .. code-block:: yaml
  
    -
    name: Create dualstack device using 'create' method
    stc:
        action: create
        under: ref:/project
        count: 1
        objects:
        - emulateddevice:
            AffiliatedPort: ref:/port[@name='Port1']
            DeviceCount: 1
            name: "ipv4_ipv6_device_1"
            PrimaryIf: ref:./Ipv4If
            TopLevelIf: ref:./Ipv4If
            EthIIIf:
              SourceMac: 00:10:96:00:00:01
            Ipv4If:
              AddrStep: 0.0.0.1
              Address: 192.168.1.2
              Gateway: 192.168.1.1
              StackedOnEndpoint-targets: ref:./EthIIIf
              TopLevelIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_device_1']
              PrimaryIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_device_1']
            Ipv6If:
              AddrStep: ::1
              Address: 2001::2
              Gateway: 2001::1
              StackedOnEndpoint-targets: ref:./EthIIIf
              TopLevelIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_device_1']
              PrimaryIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_device_1']
    
    -
    name: Create ipv6if for device 1
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name='ipv4_ipv6_device_1']
        count: 1
        objects:
        - Ipv6If:
            AddrStep: ::1
            Address: fe80::1
            PrimaryIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_device_1']
            TopLevelIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_device_1']
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_ipv6_device_1']/EthIIIf
    ##########################################################################################
    -
    name: create dualstack device using 'perform'
    stc:
        action: perform
        command: DeviceCreate
        properties:
        ParentList:  ref:/project
        CreateCount: 1
        DeviceCount: 1
        Port: ref:/port[@Name='Port2']
        IfStack: Ipv6If Ipv4If EthIIIf
        IfCount: '1 1 1'
        name: "ipv4_ipv6_device_2"
    
    -
    name: Config ipv4if address
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_device_2']/Ipv4If
        properties:
            Address: 192.168.1.1
            Gateway: 192.168.1.2
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_device_2"]
    
    -
    name: Config ipv6if address
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_device_2']/Ipv6If
        properties:
            Address: 2001::1
            Gateway: 2001::2
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv4_ipv6_device_2"]/EthIIIf
    
    -
    name: Create ipv6if
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name="ipv4_ipv6_device_2"]
        count: 1
        objects:
        - Ipv6If:
            AddrStep: ::1
            Address: fe80::1
            PrimaryIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_device_2"]
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_device_2"]
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv4_ipv6_device_2"]/EthIIIf

  9. Sample YAML code to create dualstack(IPv4IPv6) emulated device with single VLAN:
  
  .. code-block:: yaml
  
    -
    name: Create dualstack device with single vlan using 'create' method
    stc:
        action: create
        under: ref:/project
        count: 1
        objects:
        - emulateddevice:
            AffiliatedPort: ref:/port[@name='Port1']
            DeviceCount: 1
            name: "ipv4_ipv6_single_vlan_1"
            PrimaryIf: ref:./Ipv6If
            TopLevelIf: ref:./Ipv6If
            EthIIIf:
                SourceMac: 00:10:96:00:00:01
            VlanIf:
                VlanId: 100
            Ipv4If:
                AddrStep: 0.0.0.1
                Address: 192.168.1.2
                Gateway: 192.168.1.1
            Ipv6If:
                AddrStep: ::1
                Address: 2002::2
                Gateway: 2002::1
    
    -
    name: Config ipv6if Stack relation
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_1']/Ipv6If
        properties:
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_single_vlan_1"]
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv4_ipv6_single_vlan_1"]/VlanIf
    
    -
    name: Create linklocal ipv6if
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_1']
        count: 1
        objects:
        - Ipv6If:
            AddrStep: ::1
            Address: fe80::1
            PrimaryIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_1']
            TopLevelIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_1']
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_1']/VlanIf
    
    -
    name: config VlanIf stack relation
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_1']/VlanIf
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_1']/EthIIIf
    
    -
    name: config ipv4if stack relation
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_1']/Ipv4If
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_1']/VlanIf
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_single_vlan_1"]
    ###############################################################################################
    -
    name: create dualstack device with single vlan using 'perform'
    stc:
        action: perform
        command: DeviceCreate
        properties:
        ParentList:  ref:/project
        CreateCount: 1
        DeviceCount: 1
        Port: ref:/port[@Name='Port2']
        IfStack: Ipv6If Ipv4If VlanIf EthIIIf
        IfCount: '1 1 1 1'
        name: "ipv4_ipv6_single_vlan_2"
    
    -
    name: config ipv6if
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_2']/Ipv6If
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv4_ipv6_single_vlan_2"]/VlanIf
    
    -
    name: config ipv4if
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_single_vlan_2']/Ipv4If
        properties:
            Address: 192.168.1.1
            Gateway: 192.168.1.2
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_single_vlan_2"]
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv4_ipv6_single_vlan_2"]/VlanIf
    
    -
    name: Create ipv6if
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name="ipv4_ipv6_single_vlan_2"]
        count: 1
        objects:
        - Ipv6If:
            AddrStep: ::1
            Address: fe80::4
            PrimaryIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_single_vlan_2"]
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_single_vlan_2"]
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv4_ipv6_single_vlan_2"]/VlanIf

  10. Sample YAML code to create dualstack(IPv4IPv6) emulated device with double VLAN:
  
  .. code-block:: yaml
  
    -
    name: Create dualstack device with double vlan using 'create' method
    stc:
        action: create
        under: ref:/project
        count: 1
        objects:
        - emulateddevice:
            AffiliatedPort: ref:/port[@name='Port1']
            DeviceCount: 1
            name: "ipv4_ipv6_dual_vlan_1"
            PrimaryIf: ref:./Ipv6If
            TopLevelIf: ref:./Ipv6If
            EthIIIf:
                SourceMac: 00:10:96:00:00:01
            VlanIf:
                VlanId: 100
            Ipv4If:
                AddrStep: 0.0.0.1
            Address: 192.168.1.1
                Gateway: 192.168.1.2
            Ipv6If:
                AddrStep: ::1
                Address: 2002::2
                Gateway: 2002::1
    
    -
    name: create VlanIf under device 1
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']
        count: 1
        objects:
        - VlanIf:
            VlanId: 100
    
    -
    name: Create linklocal ipv6if on emulated device
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']
        count: 1
        objects:
        - Ipv6If:
            AddrStep: ::1
            Address: fe80::1
            PrimaryIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']
            TopLevelIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']
    
    -
    name: config outer VlanIf Stack relation
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']/VlanIf[1]
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']/VlanIf[0]
    
    -
    name: config Ipv4If Stack relation
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']/Ipv4If
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']/VlanIf[1]
            PrimaryIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']
            TopLevelIfSource: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']
    
    -
    name: config Ipv6If Stack relation
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']/Ipv6If[0]
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']/VlanIf[1]
    
    -
    name: config linklocal Ipv6If Stack relation
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']/Ipv6If[1]
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']/VlanIf[1]
    
    -
    name: config inner VlanIf Stack relation
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']/VlanIf[0]
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_1']/EthIIIf
    #############################################################################################
    -
    name: create dualstack device with double vlan using 'perform'
    stc:
        action: perform
        command: DeviceCreate
        properties:
        ParentList:  ref:/project
        CreateCount: 1
        DeviceCount: 1
        Port: ref:/port[@Name='Port2']
        IfStack: Ipv6If Ipv4If VlanIf VlanIf EthIIIf
        IfCount: '1 1 1 1 1'
        name: "ipv4_ipv6_dual_vlan_2"
    
    -
    name: config ipv4if
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_2']/Ipv4If
        properties:
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_dual_vlan_2"]
    
    -
    name: config ipv6if
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='ipv4_ipv6_dual_vlan_2']/Ipv6If
        properties:
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv4_ipv6_dual_vlan_2"]/VlanIf[0]
    
    -
    name: Create ipv6if
    stc:
        action: create
        under: ref:/EmulatedDevice[@Name="ipv4_ipv6_dual_vlan_2"]
        count: 1
        objects:
        - Ipv6If:
            AddrStep: ::1
            Address: fe80::5
            PrimaryIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_dual_vlan_2"]
            TopLevelIfSource: ref:/EmulatedDevice[@Name="ipv4_ipv6_dual_vlan_2"]
            StackedOnEndpoint-targets: ref:/EmulatedDevice[@Name="ipv4_ipv6_dual_vlan_2"]/VlanIf[0]

Configure Emulated Device
-------------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing Emulation device and it's sub object properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure emulated device
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         objects: <Emulated device name/tag or Emulateddeive interface path>  :mandatory:`M`
         properties:
            <attribute1: value1>
            <attribute2: value2>
            .
            .

.. raw:: html
    
   <table>
     <tr>
       <th style="text-align: center">Parameter</th>
       <th style="text-align: center">Value Type</th>
       <th style="text-align: center">Description</th>
     </tr>
     <tr>
       <td>action</td>
       <td>string</td>
       <td>Specifies the action for the given task. Here it is <code>config</code>.
           <div><b>Required:</b> Yes</div>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of emulated devices to be configured.</div>
          <div>Count value above 1, creates several emulated device objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace 
           with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>xpath</td>
       <td>
            <div>An emulated device object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>object: ref:/EmulatedDevice[@Name='Dev1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. Emulated device must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of emulated device object.</div>
          <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>properties:</code></div>
                   <div><code>DeviceCount: 1</code></div>
                   <div><code>RouterId: 1.0.0.0</code></div>
            <div><b>See Also:</b></div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/EmulatedDevice.htm'> EmulatedDevice object reference guide</a><div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/EthIIIf.htm'> EthIIIf object reference page
          </a></div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/VlanIf.htm'> VlanIf object reference page 
          </a><div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ipv4If.htm'> Ipv4If object reference page 
          </a><div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ipv6If.htm'> Ipv6If object reference page 
          </a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

  .. code-block:: yaml
  
    -
    name: config device properties
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='Dev1']
        properties:
            DeviceCount: 1
            EnablePingResponse: True
            RouterId: 1.0.0.0
            

    -
    name: config device Ipv4 properties
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='Dev1']/Ipv4If
        properties:
            Address: 10.1.1.2
            AddressStep: 0.1.0.0
            Gateway: 10.0.0.1
            GatewayStep: 0.0.0.1
            PrefixLength: 24
    
    -
    name: config device Ipv6 properties
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='Dev1']/Ipv6If
        properties:
            Address: 1000::2
            AddressStep: ::1
            Gateway: 1000::1
            GatewayStep: ::0
            PrefixLength: 64
    
    -
    name: config device single VlanIf properties
    stc:
        action: config
        objects: ref:/EmulatedDevice[@Name='Dev1']/VlanIf[0]
        properties:
            VlanId: 100
            IdStep: 1
            Priority: 1

For more examples please check `Playbooks <https://github.com/Spirent/stc-ansible/tree/master/playbooks>`_.