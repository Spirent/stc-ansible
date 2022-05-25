Routing Protocol - BGP
======================

.. contents::
   :local:
   :depth: 1

Overview
--------

`STC Ansible` module allows you to create various Border Gateway Protocol (BGP) test scenarios. 
It helps to create scaling tests with hundreds of emulated BGP routers advertising thousands of 
routes. 

To create and configure an emulated Border Gateway Protocol (BGP) test through `STC Ansible` module, 
initially you should create `BGProuterconfig` object under an emulated device. 
Once the BGP protocol is enabled on the emulated device, it will act as a BGP router.

BGP routes should be created on top of an emulated BGP router using BGP route objects.

You can configure all the characteristics of a BGP emulated router as well as the routes during 
the creation of BGP devices and routes. Same can also be reconfigured/modify later.

Once the BGP routers and routes set up is done, you can configure the Streamblock/traffic generator
between the routers or the routes by setting the source and destination BGP object references.

Now, you can verify the traffic statistics (transmitted and received packets) between the 
routers/routes by starting the devices (here emulated BGP routers).

Please refer example playbook `BGP_Traffic <https://github.com/Spirent/stc-ansible/blob/master/playbooks/bgp-traffic.yaml>`_.


Create BGP Device
-----------------

Purpose
~~~~~~~

Creates BGP object(s) in the Spirent Test Center(stc) datamodel under the emulated device object(s).
During the object creation, Name and other BGP properties can be defined.
The name of the BGP object will be used as a reference in order to reconfigure/modify
any of it's properties later.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: create bgp device
      stc: 
         action: create  :mandatory:`M`
         under: <emulated device reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <BGP object name>  :mandatory:`M`
              <BGP attribute1: value1>
              <BGP attribute2: value2>
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
            <div>An emulated device under which the BGP protocol is created.</div>
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
          <div>Specifies the number of BGP devices to be created.</div>
          <div>Count value above 1, creates several BGP objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create BGP device, use <code>BgpRouterConfig</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div>    <a href='https://kms.spirentcom.com/CSC/pabtech/stc-automation-html/BgpRouterConfig.htm'> Bgp object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: create bgp on Ipv4 Device
      stc: 
        action: create
        under: /EmulatedDevice[@Name='IPV4-Device1']
        count: 1
        objects: 
          - BgpRouterConfig: 
              IpVersion: IPV4
              AsNum: 1111
              DutAsNum: 2222
              Name: "IPV4-BGPRouter1"

    -
      name: create bgp on Ipv6 Device
      stc: 
         action: create
         under: /EmulatedDevice[@Name='IPV6-Device1']
         count: 1
         objects: 
           - BgpRouterConfig: 
              IpVersion: IPV6
              AsNum: 1111
              DutAsNum: 2222
              Name: "IPV6-BGPRouter1"

    -
      name: create 10 bgp devices
      stc: 
         action: create
         under: /EmulatedDevice[@Name='IPV6-Device${item}']
         count: 10
         objects: 
           - BgpRouterConfig: 
              IpVersion: IPV6
              AsNum: 1111
              DutAsNum: 2222
              Name: "IPV6-BGPRouter${item}"
              DutIpv4Addr: 1.1.1.${item}


Configure BGP Device
--------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing BGP objects properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure bgp device
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <BGP device reference>  :mandatory:`M`
         properties:   :mandatory:`M`
            <BGP attribute1: value1>
            <BGP attribute2: value2>
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
          <div>Specifies the number of BGP devices to be configured.</div>
          <div>Count value above 1, creates several BGP objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace 
           with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>object</td>
       <td>xpath</td>
       <td>
            <div>An emulated BGP device object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>object: ref:/EmulatedDevice[@Name='Dev1']/BgpRouterConfig[@Name='BGPDev1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. BGP device must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of BGP object.</div>
          <div><b>Required:</b> Yes</div>
          <div>For BGP attributes, please refer <div>
          <div><a href='https://kms.spirentcom.com/CSC/pabtech/stc-automation-html/BgpRouterConfig.htm'> Bgp object reference guide</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: configure/modify BGP device properties
      stc: 
      action: configure
      count: 1
      object: ref:/EmulatedDevice[@Name='Device1']/BgpRouterConfig[@Name='BGPDevice1']
      properties: 
        AsNum: 101
        DutAsNum: 102
        DutIpv4Addr: 1.1.1.1

    -
      name: configure/modify multiple BGP device properties
      stc: 
      action: configure
      count: 10
      object: ref:/EmulatedDevice[@Name='Device${item}']/BgpRouterConfig[@Name='BGPDevice${item}']
      properties: 
        AsNum: 101
        DutAsNum: 102
        DutIpv4Addr: 1.1.${item}.1


Create BGP Routes
-----------------

Purpose
~~~~~~~

Creates and configures BGP routes under a specific BGP device object.
It also defines the characteristics of the routes that will be advertised at the 
beginning of the session.

Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: create bgp route
      under: <BGP device reference path> :mandatory:`M`
      count: <integer>
      stc: 
         action: create  :mandatory:`M`
         objects:   :mandatory:`M`
           - <BGP Route Object>:
               <BGP Route attribute1: value1>
               <BGP Route attribute2: value2>
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
            <div>A BGP device under which the BGP route is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
            <div><code>under: ref:/EmulatedDevice[@Name='Dev1']/BgpRouterConfig[@Name='BGPDev1']</code></div>
            <div><b>See also:</b></div>
            <div>- <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
            <div><b>NOTES:</b></div>
            <div>1. BGP Device must already exist</div>
            <div>2. If the path is incorrect, an exception will be raised and the playbook stops. 
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of BGP routes to be created.</div>
          <div>Count value above 1, creates several BGP Route objects in an iterative way.</div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field.</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create IPv4 and IPv6 BGP routes, use <code>BgpIpv4RouteConfig</code> and <code>BgpIpv6RouteConfig</code> objects.
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/BgpIpv4RouteConfig.htm'>Bgp Ipv4 Route Object Reference Guide</a> </div>
          <div><a href='<http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/BgpIpv6RouteConfig.htm'>Bgp Ipv6 Route Object Reference Guide</a> </div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/BgpRouterConfig.htm'>BGP object Reference Guide</a> for other BGP routes creation like SRTE, LinkState, EVPN etc.</div>
       </td>
     </tr>
   </table>



Examples
~~~~~~~~

.. code-block:: yaml

   -
     name: create ipv4 route on bgp device
     stc: 
       action: create
       under: /EmulatedDevice[@Name='Device1']/BgpRouterConfig[@Name='BGPRouter1']
       count: 1
       objects: 
         - BgpIpv4RouteConfig: 
            name: "BGPV4Route1"
            AsPath: 2222
            Ipv4NetworkBlock: 
               NetworkCount: 100
               StartIpList: 2.2.2.2
          
   -
     name: create ipv6 route on bgp device
     stc: 
       action: create
       under: /EmulatedDevice[@Name='IPV6-Device1']/BgpRouterConfig[@Name='IPV6-BGPRouter1']
       count: 1
       objects: 
         - BgpIpv6RouteConfig: 
            name: "BGPV6Route1"
            AsPath: 2222
            Ipv4NetworkBlock: 
               NetworkCount: 100
               StartIpList: 2000::1

   -
     name: create 10 ipv4 routes
     stc: 
       action: create
       under: /EmulatedDevice[@Name='Device${item}']/BgpRouterConfig[@Name='BGPRouter{item}']
       count: 10
       objects: 
         - BgpIpv4RouteConfig: 
            name: "BGPV4Route${item}"
            AsPath: 2222
            Ipv4NetworkBlock: 
               NetworkCount: 100
               StartIpList: 2.${item}.2.2


Configure BGP Routes
--------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing BGP Route object and it's child objects properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure bgp route
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <BGP Route reference>  :mandatory:`M`
         properties:  :mandatory:`M`
            <BGP Route attribute1: value1>
            <BGP Route attribute2: value2>
              <Route child object>
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
          <div>Specifies the number of BGP routes to be configured.</div>
          <div>Count value above 1, creates several BGP route objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in device names. The item will be replace 
           with the values from 1 to count.</div>
           <div><b>Required:</b> No. Optional field.</div>
       </td>
     </tr>
     <tr>
       <td>object</td>
       <td>xpath</td>
       <td>
            <div>An emulated BGP route object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
            <div><code>ref:/EmulatedDevice[@Name='Dev1']/BgpRouterConfig[@Name='BGPDev1']/</code> </div>
            <div><code>BgpIpv4RouteConfig[@Name='Route1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. BGP device must already exist.</div>
                  <div>   2. If the device does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of BGP Route objects.</div>
          <div><b>Required:</b> Yes</div>
          <div><b>See Also:</b>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/BgpIpv4RouteConfig.htm'>Bgp Ipv4 Route Object Reference Guide</a> </div>
          <div><a href='<http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/BgpIpv6RouteConfig.htm'>Bgp Ipv6 Route Object Reference Guide</a> </div>
          <div><a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/BgpRouterConfig.htm'>BGP object Reference Guide</a> for other BGP routes configuration like SRTE, LinkState, EVPN etc.</div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

   -
     name: config another ipv4route on device2
     stc: 
       action: config
       count: 1
       objects: /EmulatedDevice[@Name='BGPDevice2']/BgpRouterConfig[@Name='BGPRouter2']/BgpIpv4RouteConfig[@Name='BGPV4Route']
       properties:
          AsPath: 1111
          Ipv4NetworkBlock: 
             NetworkCount: 101
             StartIpList: 3.3.3.3


Configure BGP Traffic
---------------------

Purpose
~~~~~~~

Configures the traffic between the BGP devices or routes.
About creating a bound streamblock, please refer `StreamBlock <../docs/StreamBlock.rst>`_ section and 
`Start Protocols <../docs/Start_Protocols.rst>`_, `Results <../docs/Results.rst>`_ section to 
start devices and get TX(transmitted)/RX(received) counter values.

Examples
~~~~~~~~

.. code-block:: yaml

   # To configure traffic between BGP Devices
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


   # To configure traffic between BGP IPV4 network blocks
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
                                 ref:/EmulatedDevice[@Name='Device1']/BgpRouterConfig[@Name='BGPRouter1']
                                 /BgpIpv4RouteConfig/Ipv4NetworkBlock
             DstBinding-targets: |
                                 ref:/EmulatedDevice[@Name='Device2']/BgpRouterConfig[@Name='BGPRouter2']
                                 /BgpIpv4RouteConfig/Ipv4NetworkBlock
             AffiliationStreamBlockLoadProfile: 
             Load: 10


   # To configure traffic between BGP IPV6 network blocks
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
                                 ref:/EmulatedDevice[@Name='Device1']/BgpRouterConfig[@Name='BGPRouter1']
                                 /BgpIpv6RouteConfig/Ipv6NetworkBlock
             DstBinding-targets: |
                                 ref:/EmulatedDevice[@Name='Device2']/BgpRouterConfig[@Name='BGPRouter2']
                                 /BgpIpv6RouteConfig/Ipv6NetworkBlock
             AffiliationStreamBlockLoadProfile: 
             Load: 10


For more examples please check `Playbooks <https://github.com/Spirent/stc-ansible/tree/master/playbooks>`_.