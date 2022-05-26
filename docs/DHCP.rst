Access Protocol - DHCP
======================

.. contents::
   :local:
   :depth: 1

Overview
--------

`STC-ansible` allows you to create complex tests to validate DHCP implementations.

DHCP (Dynamic Host Configuration Protocol) uses a client-server model, in which DHCP servers provide network 
addresses and configuration parameters to DHCP clients.

To create and configure a DHCP server through `STC Ansible` module, initially you should create
`DHCPv4Serverconfig` object for Ipv4 and `DHCPv6Serverconfig` object for Ipv6 under an emulated device.
 
Then, you need to configure DHCP at the port level using the object `Dhcpv4PortConfig` for IPv4 or
`Dhcpv6PortConfig` for Ipv6 under a client port. The parameters apply to all DHCP hosts (clients) 
emulated by the applicable port.

Use `Dhcpv4BlockConfig` for IPv4 or `Dhcpv6BlockConfig` for IPv6 to configure blocks of hosts for 
DHCP emulation. The parameters also configure the DHCP messages sentbetween the emulated DHCP hosts (clients)
and the DHCP server (DUT) in order to obtain an IP address. 

You can configure all the characteristics of a DHCP Server and client/session block during 
the creation. Same can also be reconfigured/modify later.

Now, you can verify the DHCP server and session results by starting the devices.

Please refer example playbooks dhcpv4-config.yaml and dhcpv6-config.yaml in
`Github <https://github.com/Spirent/stc-ansible/tree/master/playbooks>`_ link.


Create DHCPv4/v6 Server
-----------------------

Purpose
~~~~~~~

Creates DHCPv4 or DHCPv6 server object(s) in the Spirent Test Center(stc) datamodel under the emulated device object(s).
During the object creation, Name and other DHCP properties can be defined.
The name of the DHCP object will be used as a reference in order to reconfigure/modify
any of it's properties later.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: create DHCPv4/v6 device
      stc: 
         action: create  :mandatory:`M`
         under: <emulated device reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <DHCP object name>  :mandatory:`M`
              <DHCP attribute1: value1>
              <DHCP attribute2: value2>
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
            <div>An emulated device under which the DHCP Server is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>under: /EmulatedDevice[@Name=’Device1’]</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='../docs/EmulatedDevice.rst'>EmulatedDevice section</a></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. EmulatedDevice must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of DHCP Servers to be created.</div>
          <div>Count value above 1, creates several DHCP server objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create DHCPv4 Server, use <code>DHCPv4ServerConfig</code> object.</div>
          <div>To create DHCPv6 Server, use <code>DHCPv6ServerConfig</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Dhcpv4ServerConfig.htm'> DHCPv4 Server object reference guide</a><div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Dhcpv6ServerConfig.htm'> DHCPv6 Server object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: create DHCPv4 Server
      stc: 
        action: create
        under: /EmulatedDevice[@Name='Device1']
        count: 1
        objects: 
            - Dhcpv4ServerConfig: 
                HostName: server_@p-@b-@s
                LeaseTime: 3600 
                Ipv4Tos: 192
                name: "DHCPv4Server"
                dhcpv4serverdefaultpoolconfig:
                   StartIpList: 192.85.1.4

    -
      name: create DHCPv6 Server
      stc: 
        action: create
        under: /EmulatedDevice[@Name='Device1']
        count: 1
        objects: 
            - Dhcpv6ServerConfig: 
                EmulationMode: DHCPV6
                name: "DHCPv6Server"
                Dhcpv6ServerDefaultPrefixPoolConfig:
                   StartIpList: 2001::10

    -
      name: create 10 DHCPv4 Servers
      stc: 
        action: create
        under: /EmulatedDevice[@Name='Device${item}']
        count: 10
        objects: 
            - Dhcpv4ServerConfig: 
                HostName: server_${item}
                LeaseTime: 3600 
                Ipv4Tos: 192
                name: "DHCPv4Server${item}"
                dhcpv4serverdefaultpoolconfig:
                   StartIpList: 192.85.1.${item}


Configure DHCPv4/v6 Server
--------------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing DHCPv4 or DHCPv6 Server objects properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure DHCP Server
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <DHCPv4/v6 device reference>  :mandatory:`M`
         properties:   :mandatory:`M`
            <DHCP attribute1: value1>
            <DHCP attribute2: value2>
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
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of DHCP Servers to be configured.</div>
          <div>Count value above 1, creates several DHCP Server objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace 
           with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>object</td>
       <td>xpath</td>
       <td>
            <div>An emulated DHCPv4 or DHCPv6 Server object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>object: ref:/EmulatedDevice[@Name='Dev1']/DHCPv4ServerConfig[@Name='DHCPSer1']</code></div>
                   <div>OR</div>
                   <div><code>object: ref:/EmulatedDevice[@Name='Dev1']/DHCPv6ServerConfig[@Name='DHCPSer1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. DHCPv4 or DHCPv6 Server must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of DHCPv4 or DHCPv6 Server object.</div>
          <div><b>Required:</b> Yes</div>
          <div>For DHCPv4 and DHCPv6 Server attributes, please refer <div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Dhcpv4ServerConfig.htm'> DHCPv4 Server object reference guide</a><div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Dhcpv6ServerConfig.htm'> DHCPv6 Server object reference guide</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: configure/modify DHCPv4 server properties
      stc: 
      action: configure
      count: 1
      object: ref:/EmulatedDevice[@Name='Device1']/DHCPv4ServerConfig[@Name='DHCPSer1']
      properties: 
        HostName: server_1
        LeaseTime: 3200 
        Ipv4Tos: 190
        dhcpv4serverdefaultpoolconfig:
           StartIpList: 192.85.1.6

    -
      name: configure/modify DHCPv6 server properties
      stc: 
      action: configure
      count: 1
      object: ref:/EmulatedDevice[@Name='Device1']/DHCPv6ServerConfig[@Name='DHCPv6Ser1']
      properties: 
        EmulationMode: DHCPV6_PD
        Dhcpv6ServerDefaultPrefixPoolConfig:
           StartIpList: 2001::11

    -
      name: configure/modify multiple DHCPv4 Server properties
      stc: 
      action: configure
      count: 10
      object: ref:/EmulatedDevice[@Name='Device${item}']/DHCPv4ServerConfig[@Name='DHCPv4Ser${item}']
      properties: 
        HostName: server_${item}
        LeaseTime: 3200 
        Ipv4Tos: 190
        dhcpv4serverdefaultpoolconfig:
           StartIpList: 192.85.1.${item}


Configure DHCPv4/v6 Port
------------------------

Purpose
~~~~~~~

Configures an existing DHCPv4 or DHCPv6 port object properties.
These characteristics applies only to the DHCPv4 or DHCPv6 client/session blocks created under
the same port.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure DHCP port
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <port reference>  :mandatory:`M`
         properties:   :mandatory:`M`
            <DHCP attribute1: value1>
            <DHCP attribute2: value2>
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
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of DHCPv4 or DHCPv6 ports to be configured.</div>
          <div>Count value above 1, creates several DHCP port objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace 
           with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>object</td>
       <td>xpath</td>
       <td>
            <div>A DHCPv4 or DHCPv6 port object under which the attributes need to be configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>object: ref:/Port[@Name='Port1']/Dhcpv4PortConfig</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. A port must already exist.</div>
                  <div>   2. If the port does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of DHCPv4 or DHCPv6 port object.</div>
          <div><b>Required:</b> Yes</div>
          <div>For DHCPv4 and DHCPv6 Port attributes, please refer <div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Dhcpv4PortConfig.htm'> DHCPv4 Port object reference guide</a><div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Dhcpv6PortConfig.htm'> DHCPv6 Port object reference guide</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: configure DHCPv4 port properties
      stc: 
      action: configure
      count: 1
      object: ref:/Port[@Name='Port1']/DHCPv4PortConfig
      properties: 
        LeaseTime: 60
        ReleaseTimeout: 1

    -
      name: configure DHCPv6 port properties
      stc: 
      action: configure
      count: 1
      object: ref:/Port[@Name='Port1']/DHCPv6PortConfig
      properties: 
        LeaseTime: 60
        ReleaseTimeout: 2


Create DHCPv4/v6 Session Block
------------------------------

Purpose
~~~~~~~

Creates DHCPv4 or DHCPv6 sessions block object(s) in the Spirent Test Center(stc) datamodel under the emulated device object(s).
During the object creation, Name and other DHCP session properties can be defined.
The name of the DHCP object will be used as a reference in order to reconfigure/modify
any of it's properties later.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: create DHCPv4/v6 session block
      stc: 
         action: create  :mandatory:`M`
         under: <emulated device reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <DHCP object name>  :mandatory:`M`
              <DHCP attribute1: value1>
              <DHCP attribute2: value2>
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
            <div>An emulated device under which the DHCP Session block is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>under: /EmulatedDevice[@Name=’Device1’]</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='../docs/EmulatedDevice.rst'>EmulatedDevice section</a></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. EmulatedDevice must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of DHCP Session blocks to be created.</div>
          <div>Count value above 1, creates several DHCP session block objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create DHCPv4 Session block, use <code>DHCPv4BlockConfig</code> object.</div>
          <div>To create DHCPv6 Session block, use <code>DHCPv6BlockConfig</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Dhcpv4BlockConfig.htm'> DHCPv4 session block object reference guide</a><div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Dhcpv6BlockConfig.htm'> DHCPv6 session block object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml


    -
      name: create DHCPv4 session block on the device2
      stc: 
        action: create
        under: ref:/EmulatedDevice[@Name='Device2']
        count: 1
        objects: 
           - Dhcpv4BlockConfig: 
               UsesIf-targets: ref:/EmulatedDevice[@Name='Device2']/Ipv4if
               HostName: client_@p-@b-@s
               name: "DHCPv4sessionblock"

    -
      name: create DHCPv6 session block on the device2
      stc: 
        action: create
        under: ref:/EmulatedDevice[@Name='Device2']
        count: 1
        objects: 
           - Dhcpv6BlockConfig: 
               UsesIf-targets: ref:/EmulatedDevice[@Name='Device2']/Ipv6if
               Dhcpv6ClientMode: DHCPV6
               name: "DHCPv6sessionblock"

    -
      name: create 10 DHCPv4 session blocks
      stc: 
        action: create
        under: ref:/EmulatedDevice[@Name='Device${item}']
        count: 10
        objects: 
           - Dhcpv4BlockConfig: 
               UsesIf-targets: ref:/EmulatedDevice[@Name='Device${item}']/Ipv4if
               HostName: client_${item}
               name: "DHCPv4sessionblock${item}"


Configure DHCPv4/v6 Session Blocks
----------------------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing DHCPv4 or DHCPv6 Session block objects properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure DHCP Session block
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <DHCPv4/v6 device reference>  :mandatory:`M`
         properties:   :mandatory:`M`
            <DHCP attribute1: value1>
            <DHCP attribute2: value2>
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
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of DHCP Session block to be configured.</div>
          <div>Count value above 1, creates several DHCP Session block objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace 
           with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>object</td>
       <td>xpath</td>
       <td>
            <div>An emulated DHCPv4 or DHCPv6 Session block object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>object: ref:/EmulatedDevice[@Name='Dev1']/DHCPv4BlockConfig[@Name='DHCPblock1']</code></div>
                   <div>OR</div>
                   <div><code>object: ref:/EmulatedDevice[@Name='Dev1']/DHCPv6BlockConfig[@Name='DHCPblock1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. DHCPv4 or DHCPv6 Session block object must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of DHCPv4 or DHCPv6 Session block object.</div>
          <div><b>Required:</b> Yes</div>
          <div>For DHCPv4 and DHCPv6 Session block attributes, please refer <div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Dhcpv4BlockConfig.htm'> DHCPv4 session block object reference guide</a><div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Dhcpv6BlockConfig.htm'> DHCPv6 session block object reference guide</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: configure/modify DHCPv4 session block properties
      stc: 
      action: configure
      count: 1
      object: ref:/EmulatedDevice[@Name='Device1']/DHCPv4BlockConfig[@Name='DHCPblock1']
      properties: 
        HostName: client_@p-@b-@s

    -
      name: configure/modify DHCPv6 session block properties
      stc: 
      action: configure
      count: 1
      object: ref:/EmulatedDevice[@Name='Device1']/DHCPv6BlockConfig[@Name='DHCPv6block1']
      properties: 
          Dhcpv6ClientMode: DHCPV6

    -
      name: configure/modify multiple DHCPv4 session block properties
      stc: 
      action: configure
      count: 10
      object: ref:/EmulatedDevice[@Name='Device${item}']/DHCPv4BlockConfig[@Name='DHCPv4block${item}']
      properties: 
        HostName: client_${item}


Please refer `Start Protocols <../docs/Start_Protocols.rst>`_ and `Results <../docs/Results.rst>`_ sections 
to start DHCP devices and verify the session results.

