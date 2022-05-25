Switching Protocol - VXLAN
==========================

.. contents::
   :local:
   :depth: 1

Overview
--------

`STC-ansible` allows you to create Virtual eXtensible Local Area Network (VXLAN) emulated devices.

VXLAN encapsulates MAC frames in a UDP header to create a Layer 2 connection across an IP network 
between two vSphere hypervisor hosts. These hosts are known as Virtual Tunnel Endpoints (VTEPs) and 
perform the encapsulation/decapsulation function for the tunnel. VXLAN uses IP multicast to associate 
a VM MAC address with a VTEP IP address.

`STC ansible` helps to construct VTEPs, VMs, and traffic for a VXLAN test.

Please refer example playbooks vxlan-bgp-evpn-config.yaml in
`Github <https://github.com/Spirent/stc-ansible/tree/master/playbooks>`_ link.


Create VTEP Device
------------------

Purpose
~~~~~~~

Creates VXLAN Tunnel End Point (VTEP) object(s) in the Spirent Test Center(stc) datamodel under the emulated device object(s).
During the object creation, Name and other VTEP properties can be defined.
The name of the VTEP object will be used as a reference in order to reconfigure/modify
any of it's properties later.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: create VTEP device
      stc: 
         action: create  :mandatory:`M`
         under: <emulated device reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <VTEP object name>  :mandatory:`M`
              <VTEP attribute1: value1>
              <VTEP attribute2: value2>
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
            <div>An emulated device under which the VTEP is created.</div>
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
          <div>Specifies the number of VTEP's to be created.</div>
          <div>Count value above 1, creates several VTEP objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create VTEP, use <code>VxlanVtepConfig</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/VxlanVtepConfig.htm'> VXLAN VTEP object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: Create Vxlan VTEP config 1
      stc:
        action: create
        under: ref:/project/Emulateddevice[@Name='VTEP Device']
        count: 1
        objects:
          - VxlanVtepConfig:
             Name: "VxlanVtep_1"
             AutoSelectUdpSrcPort: "true"
             MulticastType: MULTICAST_IGMP
             UdpChecksumEnabled: "false"
             UsesIf-targets: ref:/project/Emulateddevice[@Name='VTEP Device']/Ipv4If[0]

    -
      name: Create multiple Vxlan VTEP's
      stc:
        action: create
        under: ref:/project/Emulateddevice[@Name='VTEP Device${item}']
        count: 10
        objects:
          - VxlanVtepConfig:
             Name: "VxlanVtep_${item}"
             AutoSelectUdpSrcPort: "true"
             MulticastType: MULTICAST_IGMP
             UdpChecksumEnabled: "false"
             UsesIf-targets: ref:/project/Emulateddevice[@Name='VTEP Device${item}']/Ipv4If[0]


Create Vxlan Interface
----------------------

Purpose
~~~~~~~

Creates Vxlan interface on VTEP enabled Emulated device object(s).

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: create Vxlanif
      stc: 
         action: create  :mandatory:`M`
         under: <emulated device reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <Vxlan interface object name>  :mandatory:`M`
              <Vxlan interface attribute1: value1>
              <Vxlan interface attribute2: value2>
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
            <div>An emulated device under which the Vxlan interface object is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>under: /EmulatedDevice[@Name=’Device1’]</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='../docs/EmulatedDevice.rst'>EmulatedDevice section</a></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. A VTEP enabled EmulatedDevice must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of Vxlan interface objects to be created.</div>
          <div>Count value above 1, creates several VxlanIf objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create Vxlan interface, use <code>VxlanIf</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/VxlanIf.htm'> Vxlan interface object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: Create Vxlanif
      stc:
        action: create
        under: ref:/Emulateddevice[@Name='VTEP 1']
        count: 1
        objects:
           - VxlanIf:
               StackedOnEndpoint-targets: ref:/project/Emulateddevice[@Name='VTEP 1']/Ipv4If[0]


Create VXLAN Segment
--------------------

Purpose
~~~~~~~

Creates VXLAN Segment object(s) under the project object.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: Create VXLAN Segment
      stc: 
         action: create  :mandatory:`M`
         under: <project reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <Vxlan segment object name>  :mandatory:`M`
              <Vxlan segment attribute1: value1>
              <Vxlan segment attribute2: value2>
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
            <div>Project reference under which the Vxlan Segment object is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>under: /project</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. If the reference path does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of Vxlan Segment objects to be created.</div>
          <div>Count value above 1, creates several Vxlan segment objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create Vxlan segments, use <code>VxlanSegmentConfig</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/VxlanSegmentConfig.htm'> Vxlan Segment object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: Create Vxlan Segment
      stc:
         action: create
         under: ref:/project
         count: 1
         objects:
           - VxlanSegmentConfig:
               Name: "Segment_1"
               CommunicationType: EVPN_LEARNING
               Vni: 100


    -
      name: Create multiple Vxlan Segments
      stc:
         action: create
         under: ref:/project
         count: 10
         objects:
           - VxlanSegmentConfig:
               Name: "Segment_${item}"
               CommunicationType: EVPN_LEARNING
               Vni: 10${item}


Create VXLAN VM Info
--------------------

Purpose
~~~~~~~

Creates VXLAN VM configuration object(s) under the project object.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: Create VXLAN VM config
      stc: 
         action: create  :mandatory:`M`
         under: <project reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <Vxlan VM config object name>  :mandatory:`M`
              <Vxlan VM config attribute1: value1>
              <Vxlan VM config attribute2: value2>
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
            <div>Project reference under which the Vxlan VM config object is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>under: /project</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. If the reference path does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of Vxlan VM configuration objects to be created.</div>
          <div>Count value above 1, creates several Vxlan VM configuration objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create Vxlan VM configuration, use <code>VxlanVMInfo</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/VxlanVmInfo.htm'> Vxlan VM config object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: Create Vxlan VMinfo
      stc:
        action: create
        under: ref:/project
        count: 1
        objects:
          - VxlanVmInfo:
              Name: "VM_info_1"
              UseAttachedVtepIpAddr: "false"


Config VXLAN VM Info
--------------------

Purpose
~~~~~~~

Configures an existing VXLAN VM Info objects properties and the mapping of 
VXLAN Segments to the VM Info objects.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure VM Info
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <VXLAN VM Info reference>  :mandatory:`M`
         properties:   :mandatory:`M`
            <VXLAN VM Info attribute1: value1>
            <VXLAN VM Info attribute2: value2>
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
          <div>Specifies the number of VXLAN VM Info objects to be configured.</div>
          <div>Count value above 1, creates several VXLAN VM Info objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace 
           with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>object</td>
       <td>xpath</td>
       <td>
            <div>A VXLAN VM Info object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>object: /project/VxlanVmInfo[@Name='VM_info_1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. VXLAN VM Info object must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of VXLAN VM Info object object.</div>
          <div><b>Required:</b> Yes</div>
          <div>For VXLAN VM Info object attributes and possible relations, please refer <div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/VxlanVmInfo.htm'> VXLAN VM Info object reference guide</a><div>
       </td>
     </tr>
   </table>

Examples
~~~~~~~~

1. To map VXLAN Seqments with VXLAN VM Info objects,

.. code-block:: yaml

    -
      name: Config VM info 1
      stc:
        action: config
        objects: ref:/project/VxlanVmInfo[@Name='VM_info_1']
        properties:
           MemberOfVxlanSegment-Sources: ref:/project/VxlanSegmentConfig[@Name='Segment_1']


2. To configures other properties,

.. code-block:: yaml

    -
      name: Config VM info 1
      stc:
        action: config
        objects: ref:/project/VxlanVmInfo[@Name='VM_info_1']
        properties:
           UseAttachedVtepIpAddr: FALSE
           UseL3VniForTraffic: FALSE


Config VM device
----------------

Purpose
~~~~~~~

Configures VM host with required mappings.

1. Map VM device (An emulated device must already be created) with Vxlan VM configuration.


.. code-block:: yaml

    -
      name: Config host1
      stc:
        action: config
        objects: ref:/project/EmulatedDevice[@Name='VM 1']
        properties:
           UsesVxlanVmInfo-targets: ref:/project/VxlanVmInfo[@Name='VM_info_1']

2. Create "VXLAN VM to VTEP Device Link" between VTEP and VM devices and configure link source 
   and destination interfaces.
   
.. code-block:: yaml

    -
      name: Create Link
      stc:
        action: perform
        command: LinkCreate
        properties:
            SrcDev: ref:/project/EmulatedDevice[@Name='VM Device 1']
            DstDev: ref:/project/Emulateddevice[@Name='VTEP Device 1']
            LinkType: "VXLAN VM to VTEP Device Link"

    -
      name: Config host1
      stc:
        action: config
        objects: ref:/project/EmulatedDevice[@Name='VM Device 1']
        properties:
           ContainedLink-targets: ref:/project/EmulatedDevice[@Name='VM Device 1']/vxlanvmtovteplink
       
    -
      name: Config host1
      stc:
        action: config
        objects: ref:/project/EmulatedDevice[@Name='VM Device 1']/vxlanvmtovteplink
        properties:
           LinkSrc-targets: ref:/EmulatedDevice[@Name='VM Device 1']/EthIIIf[0]
           LinkDst-targets: ref:/EmulatedDevice[@Name='VTEP Device 1']/VxlanIf[0]
       
Enable Routing Protocol on VTEP Device
--------------------------------------

To enable routing protocols like BGP on the VTEP device, need to create protocol objects under
the VTEP enabled emulated device(s).

Example to enable BGP on VTEP device,

.. code-block:: yaml

    -
      name: Enable BGP on VTEP Device 1
      stc: 
        action: create
        under: ref:/EmulatedDevice[@Name='VTEP Device 1']
        count: 1
        objects: 
         - BgpRouterConfig: 
            IpVersion: IPV4
            AsNum: 1
            DutAsNum: 1
            name: "BGPRouter1"


Configure VXLAN Traffic
-----------------------

Purpose
~~~~~~~

Configures the traffic between the VXLAN VM devices.
About creating a bound streamblock, please refer `StreamBlock <../docs/StreamBlock.rst>`_ section and 
`Start Protocols <../docs/Start_Protocols.rst>`_, `Results <../docs/Results.rst>`_ sections to 
start devices and get TX(transmitted)/RX(received) counter values.

Examples
~~~~~~~~

.. code-block:: yaml

   # To configure traffic between VM Devices
   -
     name: Configure the traffic generator1
     stc: 
       count: 1
       action: create
       under: /project
       objects: 
          - StreamBlock: 
             EnableStreamOnlyGeneration: true
             SrcBinding-targets: ref:/EmulatedDevice[@Name='VM Device 1']/Ipv4If
             DstBinding-targets: ref:/EmulatedDevice[@Name='VM Device 2']/Ipv4If
             AffiliationStreamBlockLoadProfile: 
             Load: 10

