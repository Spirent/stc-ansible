Routing Protocol - OSPF
=======================

.. contents::
   :local:
   :depth: 1

Overview
--------

`STC Ansible` module allows you to create various Open Shortest Path First (OSPF) Protocol test scenarios. 
It helps to create scaling tests with hundreds of emulated OSPF routers advertising thousands of 
Link-state advertisements (LSAs). 

To create and configure an emulated OSPF Protocol test through `STC Ansible` module, 
initially you should create `Ospfv2routerconfig` object for OSPF v2 or `Ospfv3routerconfig` object for OSPF v3 
under an emulated device. Once the OSPF protocol is enabled on the emulated device, it will act as a OSPF router.

OSPF LSAs should be created on top of an emulated OSPF router using different LSA objects.

You can configure all the characteristics of a OSPF emulated router as well as the LSAs during 
the creation of OSPF devices and LSAs. Same can also be reconfigured/modify later.

Once the OSPF routers and LSAs set up is done, you can configure the Streamblock/traffic generator
between the routers or the LSAs by setting the source and destination OSPF object references.

Now, you can verify the traffic statistics (transmitted and received packets) between the 
routers/LSAs by starting the devices (here emulated OSPF routers).

Please refer example playbooks ospfv2-traffic.yaml and ospfv3-traffic.yaml in
`Github <https://github.com/Spirent/stc-ansible/tree/master/playbooks>`_ link.


Create OSPF Device
------------------

Purpose
~~~~~~~

Creates OSPF object(s) in the Spirent Test Center(stc) datamodel under the emulated device object(s).
During the object creation, Name and other OSPF properties can be defined.
The name of the OSPF object will be used as a reference in order to reconfigure/modify
any of it's properties later.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: create OSPF device
      stc: 
         action: create  :mandatory:`M`
         under: <emulated device reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <OSPF object name>  :mandatory:`M`
              <OSPF attribute1: value1>
              <OSPF attribute2: value2>
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
            <div>An emulated device under which the OSPF protocol is created.</div>
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
          <div>Specifies the number of OSPF devices to be created.</div>
          <div>Count value above 1, creates several OSPF objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create OSPF version 2 device, use <code>Ospfv2RouterConfig</code> object.</div>
          <div>To create OSPF version 3 device, use <code>Ospfv3RouterConfig</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv2RouterConfig.htm'> OSPF v2 object reference guide</a><div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv3RouterConfig.htm'> OSPF v3 object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: create OSPF v2 on Ipv4 Device
      stc: 
        action: create
        under: /EmulatedDevice[@Name='IPV4-Device1']
        count: 1
        objects: 
          - Ospfv2RouterConfig: 
              AreaId: 0.0.0.0
              NetworkType: P2P
              HelloInterval: 20
              Name: "OSPFv2Router1"

    -
      name: create OSPF v3 on Ipv6 Device
      stc: 
         action: create
         under: /EmulatedDevice[@Name='IPV6-Device1']
         count: 1
         objects: 
           - Ospfv3RouterConfig: 
              AreaId: 0.0.0.0
              NetworkType: P2P
              HelloInterval: 20
              Name: "OSPFv3Router1"

    -
      name: create 10 OSPF devices with different area id's
      stc: 
         action: create
         under: /EmulatedDevice[@Name='Device${item}']
         count: 10
         objects: 
           - Ospfv2RouterConfig: 
              AreaId: 0.0.0.${item}
              NetworkType: P2P
              HelloInterval: 20
              Name: "IPV6-OSPFRouter${item}"


Configure OSPF Device
---------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing OSPF objects properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure OSPF device
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <OSPF device reference>  :mandatory:`M`
         properties:   :mandatory:`M`
            <OSPF attribute1: value1>
            <OSPF attribute2: value2>
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
          <div>Specifies the number of OSPF devices to be configured.</div>
          <div>Count value above 1, creates several OSPF objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace 
           with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>object</td>
       <td>xpath</td>
       <td>
            <div>An emulated OSPF device object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>object: ref:/EmulatedDevice[@Name='Dev1']/Ospfv2RouterConfig[@Name='OSPFDev1']</code></div>
                   <div><code>object: ref:/EmulatedDevice[@Name='Dev1']/Ospfv3RouterConfig[@Name='OSPFDev1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. OSPFv2 or OSPFv3 device must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of OSPF objects.</div>
          <div><b>Required:</b> Yes</div>
          <div>For OSPF attributes, please refer <div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv2RouterConfig.htm'> OSPF v2 object reference guide</a><div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv3RouterConfig.htm'> OSPF v3 object reference guide</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: configure/modify OSPFv2 device properties
      stc: 
      action: config
      count: 1
      object: ref:/EmulatedDevice[@Name='Device1']/Ospfv2RouterConfig[@Name='OSPFDevice1']
      properties: 
         AreaId: 0.0.0.1
         NetworkType: P2P
         HelloInterval: 10

    -
      name: configure/modify OSPFv3 device properties
      stc: 
      action: config
      count: 1
      object: ref:/EmulatedDevice[@Name='Device1']/Ospfv3RouterConfig[@Name='OSPFDevice1']
      properties: 
         AreaId: 0.0.0.1
         NetworkType: P2P
         HelloInterval: 10

    -
      name: configure/modify multiple OSPF device properties
      stc: 
      action: configure
      count: 10
      object: ref:/EmulatedDevice[@Name='Device${item}']/Ospfv2RouterConfig[@Name='OSPFDevice${item}']
      properties: 
         AreaId: 0.0.0.${item}
         NetworkType: P2P
         HelloInterval: 10


Create OSPF LSAs
----------------

Purpose
~~~~~~~

Creates and configures different types of OSPF LSAs under a specific OSPF device object.
It also defines the characteristics of the LSA's that will be advertised at the 
beginning of the session.

Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: create OSPF LSA
      under: <OSPF device reference path> :mandatory:`M`
      count: <integer>
      stc: 
         action: create  :mandatory:`M`
         objects:   :mandatory:`M`
           - <OSPF LSA Object>:
               <OSPF LSA attribute1: value1>
               <OSPF LSA attribute2: value2>
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
            <div>A OSPF device under which the OSPF LSA is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
            <div><code>under: /EmulatedDevice[@Name='Dev1']/Ospfv2RouterConfig[@Name='OSPFDev1']</code></div>
            <div>OR</div>
            <div><code>under: ref:/EmulatedDevice[@Name='Dev1']/Ospfv3RouterConfig[@Name='OSPFDev1']</code></div>
            <div><b>See also:</b></div>
            <div>- <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
            <div><b>NOTES:</b></div>
            <div>1. OSPF v2 or OSPF v3 Device must already exist</div>
            <div>2. If the path is incorrect, an exception will be raised and the playbook stops. 
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of OSPF routes to be created.</div>
          <div>Count value above 1, creates several OSPF Route objects in an iterative way.</div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field.</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create Router LSAs under OSPF v2 and OSPF v3 routers, use <code>RouterLsa</code> and <code>Ospfv3RouterLsa</code> objects.
          <div>To create AS-External Prefix LSA under OSPF v2 and OSPF v3 routers, use <code>ExternalLsablock</code> and <code>Ospfv3AsExternalLsaBlock</code> objects.
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/RouterLsa.htm'>OSPF v2 RouterLSA Object Reference Guide</a> </div>
          <div><a href='<http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv3RouterLsa.htm'>OSPF v3 RouterLSA Object Reference Guide</a> </div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/ExtendedLinkLsa.htm'>OSPF v2 ExtendedLinkLsa Object Reference Guide</a> </div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv3AsExternalLsaBlock.htm'>OSPF v3 Ospfv3AsExternalLsaBlock Object Reference Guide</a> </div>
          <div> Refer <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv2RouterConfig.htm'> OSPF v2 object reference guide</a><div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv3RouterConfig.htm'> OSPF v3 object reference guide</a> for other OSPF LSAs creation like Network LSA, Summary LSA etc.</div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

  1. Sample YAML code to Router LSA on OSPF v2 device:
  
  .. code-block:: yaml

   -
     name: create Router LSA on Ospf v2 device
     stc: 
       action: create
       under: /EmulatedDevice[@Name='Device1']/Ospfv2RouterConfig[@Name='Ospfv2Router1']
       count: 1
       objects: 
         - RouterLsa: 
            name: "LSA1"
            AdvertisingRouterId: 1.1.1.1
            Abr: FALSE
            LinkStateId: 2.2.2.2
            RouterLsaLink: 
               LinkCount: 10
               LinkType: POINT_TO_POINT
          
  2. Sample YAML code to Router LSA on OSPF v3 device:
  
  .. code-block:: yaml
  
   -
     name: create Router LSA on Ospf v3 device
     stc: 
       action: create
       under: /EmulatedDevice[@Name='IPV6-Device1']/Ospfv3RouterConfig[@Name='Ospfv3Router1']
       count: 1
       objects: 
         - Ospfv3RouterLsa: 
            name: "LSA1"
            AdvertisingRouterId: 1.1.1.1
            Abr: FALSE
            LinkStateId: 1
            Ospfv3RouterLsaIf: 
               IfType: POINT_TO_POINT
               NeighborRouterId: 1.1.1.1
               Ospfv3Srv6EndXSidSubTlv:
                  Algorithm: 1
                  SID: aaaa:1:1:1::

  3. Sample YAML code to NSSA LSA on OSPF v2 device:
  
  .. code-block:: yaml
  
    -
      name: create NSSA on OSPF v2 device
      stc: 
        action: create
        under: /EmulatedDevice[@Name='OSPFDevice1']/Ospfv2RouterConfig[@Name='OSPFRouter1']
        count: 1
        objects: 
        - ExternalLsaBlock: 
            name: "NSSA1"
            Ipv4NetworkBlock: 
               NetworkCount: 10
               StartIpList: 2.2.2.2

  4. Sample YAML code to NSSA LSA on OSPF v3 device:
  
  .. code-block:: yaml
  
    -
      name: create NSSA on OSPF v3 device
      stc: 
        action: create
        under: /EmulatedDevice[@Name='Ipv6-OSPFDevice1']/Ospfv3RouterConfig[@Name='OSPFRouter1']
        count: 1
        objects: 
        - Ospfv3AsExternalLsaBlock: 
            name: "NSSA1"
            Ipv6NetworkBlock: 
               NetworkCount: 10
               StartIpList: 3000::1

  5. Sample YAML code to create multiple Router LSAs on OSPF v2 device:
  
  .. code-block:: yaml
  
   -
     name: create 10 Ospf v2 LSAs
     stc: 
       action: create
       under: /EmulatedDevice[@Name='Device${item}']/Ospfv2RouterConfig[@Name='OSPFRouter${item}']
       count: 10
       objects: 
         - RouterLsa: 
            name: "LSA1"
            AdvertisingRouterId: 1.1.1.${item}
            Abr: FALSE
            LinkStateId: 2.2.2.${item}
            RouterLsaLink: 
               LinkCount: 10
               LinkType: POINT_TO_POINT


Configure OSPF LSAs
-------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing OSPF v2 or v3 LSA object and it's child objects properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure OSPF LSA
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <OSPF LSA reference>  :mandatory:`M`
         properties:  :mandatory:`M`
            <OSPF LSA attribute1: value1>
            <OSPF LSA attribute2: value2>
              <LSA child object>
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
          <div>Specifies the number of OSPF LSAs to be configured.</div>
          <div>Count value above 1, creates several OSPF LSA objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace 
           with the values from 1 to count.</div>
           <div><b>Required:</b> No. Optional field.</div>
       </td>
     </tr>
     <tr>
       <td>object</td>
       <td>xpath</td>
       <td>
            <div>An emulated OSPF LSA object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
            <div><code>ref:/EmulatedDevice[@Name='Dev1']/Ospfv2RouterConfig[@Name='OSPFDev1']/</code> </div>
            <div><code>ExternalLsablock[@Name='NSSA-Route1']</code></div>
            <div>OR</div>
            <div><code>ref:/EmulatedDevice[@Name='Dev1']/Ospfv3RouterConfig[@Name='OSPFDev1']/</code> </div>
            <div><code>Ospfv3AsExternalLsaBlock[@Name='NSSA-Route1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. OSPF device must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of OSPF LSA objects.</div>
          <div><b>Required:</b> Yes</div>
          <div><b>See Also:</b>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/RouterLsa.htm'>OSPF v2 RouterLSA Object Reference Guide</a> </div>
          <div><a href='<http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv3RouterLsa.htm'>OSPF v3 RouterLSA Object Reference Guide</a> </div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/ExtendedLinkLsa.htm'>OSPF v2 ExtendedLinkLsa Object Reference Guide</a> </div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv3AsExternalLsaBlock.htm'>OSPF v3 Ospfv3AsExternalLsaBlock Object Reference Guide</a> </div>
          <div> Refer <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv2RouterConfig.htm'> OSPF v2 object reference guide</a><div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ospfv3RouterConfig.htm'> OSPF v3 object reference guide</a> for other OSPF LSAs configuration like Network LSA, Summary LSA etc.</div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

   -
     name: config NSSA LSA under OSPF v2 device
     stc: 
       action: config
       count: 1
       objects: /EmulatedDevice[@Name='OSPFDevice1']/Ospfv2RouterConfig[@Name='OSPFRouter1']/ExtendedLinkLsa[@Name='NSSA1']
       properties:
          AdvertisingRouterId: 1.1.1.1
          Ipv4NetworkBlock: 
             NetworkCount: 101
             StartIpList: 3.3.3.3

   -
     name: config NSSA LSA under OSPF v3 device
     stc: 
       action: config
       count: 1
       objects: /EmulatedDevice[@Name='OSPFDevice2']/Ospfv3RouterConfig[@Name='OSPFRouter2']/Ospfv3AsExternalLsaBlock[@Name='NSSA1']
       properties:
          AdvertisingRouterId: 1.1.1.1
          Ipv6NetworkBlock: 
             NetworkCount: 101
             StartIpList: 3000::1


Configure OSPF Traffic
----------------------

Purpose
~~~~~~~

Configures the traffic between the OSPF devices or LSAs.
About creating a bound streamblock, please refer `StreamBlock <../docs/StreamBlock.rst>`_ section and 
`Start Protocols <../docs/Start_Protocols.rst>`_, `Results <../docs/Results.rst>`_ sections to 
start devices and get TX(transmitted)/RX(received) counter values.

Examples
~~~~~~~~

.. code-block:: yaml

   # To configure traffic between OSPF Devices
   -
     name: Configure the traffic generator1
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


   # To configure traffic between OSPF v2 network blocks
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
                                 ref:/EmulatedDevice[@Name='Device1']/Ospfv2RouterConfig[@Name='OSPFRouter1']
                                 /ExternalLsablock[@Name='NSSA1']/Ipv4NetworkBlock
             DstBinding-targets: |
                                 ref:/EmulatedDevice[@Name='Device2']/Ospfv2RouterConfig[@Name='OSPFRouter2']
                                 /ExternalLsablock[@Name='NSSA2']/Ipv4NetworkBlock
             AffiliationStreamBlockLoadProfile: 
             Load: 10


   # To configure traffic between OSPF v3 network blocks
   -
     name: Configure the traffic generator3
     stc: 
       count: 1
       action: create
       under: /project
       objects: 
          - StreamBlock: 
             EnableStreamOnlyGeneration: true
             SrcBinding-targets: |
                                 ref:/EmulatedDevice[@Name='Device1']/Ospfv3RouterConfig[@Name='OSPFRouter1']
                                 /Ospfv3AsExternalLsaBlock[@Name='NSSA1']/Ipv6NetworkBlock
             DstBinding-targets: |
                                 ref:/EmulatedDevice[@Name='Device2']/Ospfv3RouterConfig[@Name='OSPFRouter2']
                                 /Ospfv3AsExternalLsaBlock[@Name='NSSA2']/Ipv6NetworkBlock
             AffiliationStreamBlockLoadProfile: 
             Load: 10

For more examples please check `Playbooks <https://github.com/Spirent/stc-ansible/tree/master/playbooks>`_.