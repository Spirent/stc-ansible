Multicast Protocol - IGMP
=========================

.. contents::
   :local:
   :depth: 1

Overview
--------

`STC Ansible` module allows you to create/configure blocks of hosts for Internet Group Management Protocol (IGMP) emulation.
The parameters also configure the messages sent between the emulated hosts (clients) and 
the router (DUT) in order to send membership reports.
IGMP versions 1, 2 and 3 are supported.

To create and configure an emulated IGMP Protocol test through `STC Ansible` module, 
initially you should create `IGMPhostconfig` object under an emulated device. Once the 
IGMP protocol is enabled on the emulated device, it will act as a IGMP host.

An IGMP host should be assosiated to a membership with a multicast group block. To create IGMP group
membership, use `IgmpGroupMembership` object.

You can configure all the characteristics of a IGMP emulated host as well as the group memberships in create mode. 
Same can also be reconfigured/modify later.

Once the IGMP hosts and group memberships set up is done, you can configure the Streamblock/traffic generator
between the hosts or the multicast groups by setting the source and destination IGMP object references.

Now, you can verify the traffic statistics (transmitted and received packets) between the 
hosts/multicast groups by starting the devices (here emulated IGMP hosts).

Please refer example playbooks igmp-config.yaml in
`Github <https://github.com/Spirent/stc-ansible/tree/master/playbooks>`_ playbook folder.


Create IGMP Host
----------------

Purpose
~~~~~~~

Creates IGMP object(s) in the Spirent Test Center(stc) datamodel under the emulated device object(s).
During the object creation, Name and other IGMP properties can be defined.
The name of the IGMP object will be used as a reference in order to reconfigure/modify
any of it's properties later.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: create IGMP host block
      stc: 
         action: create  :mandatory:`M`
         under: <emulated device reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <IGMP object name>  :mandatory:`M`
              <IGMP attribute1: value1>
              <IGMP attribute2: value2>
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
            <div>An emulated device under which the IGMP host is created.</div>
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
          <div>Specifies the number of IGMP hosts to be created.</div>
          <div>Count value above 1, creates several IGMP objects/hosts in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create IGMP version 1, 2 or 3 host blocks, use <code>IgmphostConfig</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/IgmpHostConfig.htm'> IGMP object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: create IGMP v1 on Ipv4 Device
      stc: 
        action: create
        under: /EmulatedDevice[@Name='IPV4-Device1']
        count: 1
        objects: 
          - IGMPhostConfig: 
              Active: True
              Version: IGMP_V1
              RouterAlert: TRUE
              Name: "IGMPv1Host"

    -
      name: create IGMP v2 on Ipv4 Device
      stc: 
        action: create
        under: /EmulatedDevice[@Name='IPV4-Device2']
        count: 1
        objects: 
          - IGMPhostConfig:
              Active: True
              Version: IGMP_V2
              RouterAlert: TRUE
              Name: "IGMPv2Host"

    -
      name: create IGMP v3 on Ipv4 Device
      stc: 
        action: create
        under: /EmulatedDevice[@Name='IPV4-Device3']
        count: 1
        objects: 
          - IGMPhostConfig: 
              Active: True
              Version: IGMP_V3
              RouterAlert: TRUE
              Name: "IGMPv3Host"

    -
      name: create 10 IGMP host blocks
      stc: 
         action: create
         under: /EmulatedDevice[@Name='Device${item}']
         count: 10
         objects: 
           - IGMPhostConfig: 
              Active: True
              Version: IGMP_V3
              RouterAlert: TRUE
              Name: "IGMPv3Host${item}"


Configure IGMP Host
-------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing IGMP hosts properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure IGMP device
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <IGMP device reference>  :mandatory:`M`
         properties:   :mandatory:`M`
            <IGMP attribute1: value1>
            <IGMP attribute2: value2>
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
          <div>Specifies the number of IGMP hosts to be configured.</div>
          <div>Count value above 1, creates several IGMP objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace 
           with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>object</td>
       <td>xpath</td>
       <td>
            <div>An emulated IGMP device object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>object: ref:/EmulatedDevice[@Name='Dev1']/IGMPHostConfig[@Name='IGMPDev1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. IGMP host must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of IGMP objects.</div>
          <div><b>Required:</b> Yes</div>
          <div>For IGMP attributes, please refer <div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/IgmpHostConfig.htm'> IGMP object reference guide</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: configure/modify IGMP v1/v2/v3 host properties
      stc: 
      action: config
      count: 1
      object: ref:/EmulatedDevice[@Name='Device1']/IGMPhostConfig[@Name='IGMPDevice1']
      properties: 
         Ipv4Tos: 10
         RouterAlert: FALSE

    -
      name: configure/modify multiple IGMP host properties
      stc: 
      action: config
      count: 10
      object: ref:/EmulatedDevice[@Name='Device${item}']/IGMPhostConfig[@Name='IGMPDevice${item}']
      properties: 
         Ipv4Tos: 10
         RouterAlert: FALSE


Create IGMP Group Membership
----------------------------

Purpose
~~~~~~~

Creates blocks of IGMP group memberships under a specific IGMP host object.
It also defines the characteristics of the group membership and the source pools.

Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: create IGMP group membership
      under: <IGMP host reference path> :mandatory:`M`
      count: <integer>
      stc: 
         action: create  :mandatory:`M`
         objects:   :mandatory:`M`
           - <IGMP group membership Object>:
               <IGMP group attribute1: value1>
               <IGMP group attribute2: value2>
               .
               .

Parameters
~~~~~~~~~~

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
       <td>Specifies the action for the given task. Here it is <code>create</code>.
           <div><b>Required:</b> yes</div>
       </td>
     </tr>
     <tr>
       <td>under</td>
       <td>xpath</td>
       <td>
            <div>An IGMP host under which the IGMP group membership is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
            <div><code>under: /EmulatedDevice[@Name='Dev1']/IGMPhostConfig[@Name='IGMPDev1']</code></div>
            <div><b>See also:</b></div>
            <div>- <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
            <div><b>NOTES:</b></div>
            <div>1. IGMP v1/v2/v3 host must already exist</div>
            <div>2. If the path is incorrect, an exception will be raised and the playbook stops. 
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of IGMP group memberships to be created.</div>
          <div>Count value above 1, creates several IGMP group membership objects in an iterative way.</div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field.</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create group memberships under IGMP v1/v2/v3 hosts, use <code>IgmpGroupMembership</code> object.
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/IgmpGroupMembership.htm'> IGMP group membership Object Reference Guide</a> </div>
          <div><b>NOTES:</b></div>
            <div>1. An IPv4 Multicast group must already exist. <a href='../docs/Multicast.rst'>Multicast Group </a> section</div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

  1. Sample YAML code to create IGMP group membership on IGMP v2 host:
  
  .. code-block:: yaml

   -
     name: create IGMP group membership
     stc: 
       action: create
       under: /EmulatedDevice[@Name='Device1']/IGMPhostConfig[@Name='IGMPv2host']
       count: 1
       objects: 
         - IgmpGroupMembership:
            name: "IGMPgroup1"
            DeviceGroupMapping: MANY_TO_MANY
            FilterMode: INCLUDE
            MulticastGroup: ref:/Ipv4Group[@Name='MulticastGroup1']


          
  2. Sample YAML code to create IGMP group membership on IGMP v3 host:
  
  .. code-block:: yaml

   -
     name: create IGMP group membership
     stc: 
       action: create
       under: /EmulatedDevice[@Name='Device1']/IGMPhostConfig[@Name='IGMPv3host']
       count: 1
       objects: 
         - IgmpGroupMembership:
            name: "IGMPgroup1"
            DeviceGroupMapping: MANY_TO_MANY
            FilterMode: INCLUDE
            IsSourceList: FALSE
            UserDefinedSources: FALSE
            MulticastGroup: ref:/Ipv4Group[@Name='MulticastGroup1']
            -Ipv4NetworkBlock:
               StartIpList: 192.0.1.0
               NetworkCount: 10


  3. Sample YAML code to create multiple IGMP group memberships on IGMP v2 host:
  
  .. code-block:: yaml
  
   -
     name: create 10 IGMP group memberships
     stc: 
       action: create
       under: /EmulatedDevice[@Name='Device${item}']/IGMPhostConfig[@Name='IGMPhost${item}']
       count: 10
       objects: 
         - IgmpGroupMembership:
            name: "IGMPgroup${item}"
            DeviceGroupMapping: MANY_TO_MANY
            FilterMode: INCLUDE
            IsSourceList: FALSE
            UserDefinedSources: FALSE
            MulticastGroup: ref:/Ipv4Group[@Name='MulticastGroup${item}']
            -Ipv4NetworkBlock:
               StartIpList: 192.0.${item}.0
               NetworkCount: 10


Configure IGMP group membership
-------------------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing IGMP group membership and it's child objects properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure IGMP group membership
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <IGMP group membership reference>  :mandatory:`M`
         properties:  :mandatory:`M`
            <IGMP group membership attribute1: value1>
            <IGMP group membership attribute2: value2>
              <group membership child object>
                 <attribute1: value>
                 <attribute2: value>
                 

Parameters
~~~~~~~~~~

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
           <div><b>Required:</b> Yes.</div>
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of IGMP group memberships to be configured.</div>
          <div>Count value above 1, creates several IGMP group membership objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in group membership names. The item will be replace 
           with the values from 1 to count.</div>
           <div><b>Required:</b> No. Optional field.</div>
       </td>
     </tr>
     <tr>
       <td>object</td>
       <td>xpath</td>
       <td>
            <div>An IGMP group membership object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
            <div><code>ref:/EmulatedDevice[@Name='Dev1']/IGMPhostConfig[@Name='IGMPhost1']/</code> </div>
            <div><code>IgmpGroupMembership[@Name='group1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. IGMP devices and group memberships must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of IGMP group membership objects.</div>
          <div><b>Required:</b> Yes</div>
          <div><b>See Also:</b>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/IgmpGroupMembership.htm'> IGMP group membership Object Reference Guide</a> </div>
          <div><b>NOTES:</b></div>
            <div>1. An IPv4 Multicast group must already exist. <a href='../docs/Multicast.rst'>Multicast Group </a> section</div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

   -
     name: config IGMP group membership under IGMP v3 device
     stc: 
       action: config
       count: 1
       objects: /EmulatedDevice[@Name='IGMPDevice1']/IGMPhostConfig[@Name='IGMPhost1']/IgmpGroupMembership[@Name='group1']
       properties:
          DeviceGroupMapping: ONE_TO_ONE
          FilterMode: EXCLUDE
          IsSourceList: FALSE
          UserDefinedSources: FALSE
          MulticastGroup: ref:/Ipv4Group[@Name='MulticastGroup1']
          Ipv4NetworkBlock:
            StartIpList: 193.0.1.0
            NetworkCount: 10

Configure IGMP Traffic
----------------------

Purpose
~~~~~~~

Configures the traffic between the IGMP hosts or groups.
About creating a bound streamblock, please refer `StreamBlock <../docs/StreamBlock.rst>`_ section and 
`Start Protocols <../docs/Start_Protocols.rst>`_, `Results <../docs/Results.rst>`_ sections to 
start devices and get TX(transmitted)/RX(received) counter values.

Examples
~~~~~~~~

.. code-block:: yaml

   # To configure traffic between IGMP Devices
   -
     name: Configure multicast stream
     stc: 
       count: 1
       action: create
       under: /project
       objects: 
          - StreamBlock: 
             EnableStreamOnlyGeneration: true
             SrcBinding-targets: ref:/EmulatedDevice[@Name='Device1']/Ipv4If
             DstBinding-targets: ref:/EmulatedDevice[@Name='Device2']/Ipv4If
             AffiliationStreamBlockLoadProfile: 
               Load: 10


   # To configure traffic between IGMP groups
   -
     name: Configure the traffic generator2
     stc: 
       count: 1
       action: create
       under: /project
       objects: 
          - StreamBlock: 
             EnableStreamOnlyGeneration: true
             SrcBinding-targets: |
                                 ref:/EmulatedDevice[@Name='Device1']/IGMPhostConfig[@Name='IGMPhost1']
                                 /IgmpGroupMembership[@Name='group1']/Ipv4NetworkBlock
             DstBinding-targets: |
                                 ref:/EmulatedDevice[@Name='Device2']/IGMPhostConfig[@Name='IGMPhost2']
                                 /IgmpGroupMembership[@Name='group2']/Ipv4NetworkBlock
             AffiliationStreamBlockLoadProfile: 
               Load: 10

For more examples please check `Playbooks <https://github.com/Spirent/stc-ansible/tree/master/playbooks>`_.