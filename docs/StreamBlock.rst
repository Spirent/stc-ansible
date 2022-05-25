StreamBlock
===========

.. contents::
   :local:
   :depth: 1

Overview
--------

STC Ansible allows to create a stream block or group of stream blocks of network traffic on the specified test port(s) or project. 
A stream is a series of packets that can be tracked by STC Ansible. A stream block is a collection 
of one or more streams represented by a base stream definition plus one or more rules that describe 
how the base definition is modified to produce additional streams.

To create a stream block, use `StreamBlock` object under the project or the port.

Stream blocks are associated with a port. A port traffic generator sends traffic that is characterized 
by the stream blocks that are associated with the port.

A stream block defines the characteristics of traffic, such as frame size, QoS parameters and traffic rate. 
Spirent TestCenter has two types of stream blocks: bound and raw. The characteristics of both 
bound and raw stream blocks can be configured using STC Ansible in `create` and `config` modes.

A bound stream block is associated with specific source/destination endpoints (devices). 
Use bound stream blocks when the test involves creating devices, such as hosts or routers, 
and you want to use the addresses already specified in the stream blocks without having to configure them again.

When you configure devices (`Emulated Device <../docs/EmulatedDevice.rst>`_, 
`BGP Device <../docs/BGP.rst>`_), you can specify L2, L3 and L4 address/port, VLAN tags, MPLS labels and 
other parameters for the devices. 
When you create a bound stream block and identify the source and destination devices, Spirent TestCenter 
uses the values configured for the devices to populate the frame headers. When you change device parameters, 
such as the L2 or L3 address in a configuration that uses bound stream blocks, the stream blocks are 
automatically updated with the change. If the values are negotiated dynamically, such as through ARP/ND, 
DHCP or MPLS label negotiation, the appropriate header fields are automatically updated for a bound stream block.

When defining a raw stream block, you specify header information, such as source/destination addresses, 
at the time you configure the stream block instead of associating the block with a device. 

Use raw stream blocks when the test is focused specifically on traffic and does not include device behavior,
such as testing protocols (access, routing, multicast, etc.). 

Then, you can verify the traffic statistics (`Results <../docs/Results.rst>`_) between the 
devices by starting the traffic.

Create Stream Block
-------------------

Purpose
~~~~~~~

Creates stream block object(s) in the Spirent Test Center(stc) datamodel under the project
or any created port object(s).
During the object creation, requires to configure it's characteristics like name, Source and destination
targets etc.
The name of the stream block object will be used as a reference in order to reconfigure/modify
any of it's properties later.


.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.


.. parsed-literal::
   
   -
      name: create stream block
      stc: 
         action: create  :mandatory:`M`
         under: <project or port object reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <stream block object name>  :mandatory:`M`
                <stream block attribute1: value1>
                <stream block attribute2: value2>
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
            <div>A project or a port reference under which a stream block is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>under: /project</code></div>
                   or
                   <div><code>under: ref:/Port[@Name='Port1']</code></div>
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
          <div>Specifies the number of stream blocks to be created.</div>
          <div>Count value above 1, creates several stream block objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in stream block object names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create stream block, use <code>StreamBlock</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/StreamBlock.htm'> StreamBlock object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

  1. Sample YAML code to create a stream block under project:
  
  .. code-block:: yaml

    - 
      name: Create a stream block
      stc: 
        action: create
        under: ref:/project
        objects: 
          - streamblock: 
              Name: "sb1"
              TrafficPattern: PAIR
              EnableBidirectionalTraffic: True
              EnableStreamOnlyGeneration: true
              SrcBinding-targets: ref:/EmulatedDevice[@Name='Dev1']/Ipv4If
              DstBinding-targets: ref:/EmulatedDevice[@Name='Dev2']/Ipv4If
              AffiliationStreamBlockLoadProfile:
              Load: 10

  2. Sample YAML code to create a stream block with mesh traffic under port:
  
  .. code-block:: yaml

    - 
      name: Create traffic between emulated device end points
      stc: 
        action: create
        under: ref:/Port[@Name='Port1']
        objects: 
          - streamblock: 
              Name: "sb1"
              TrafficPattern: MESH
              EnableBidirectionalTraffic: True
              EnableStreamOnlyGeneration: true
              SrcBinding-targets: ref:/EmulatedDevice[@Name='Dev1']/Ipv4If
              DstBinding-targets: ref:/EmulatedDevice[@Name='Dev2']/Ipv4If
              AffiliationStreamBlockLoadProfile:
              Load: 10

  3. Sample YAML code to create a stream block with UDP header and it's modifiers:
  
  .. code-block:: yaml

    - 
    name: Create udp header under streamblock
    stc: 
        action: create
        under: /Port[@Name='Port1']/Streamblock[@Name='sb1']
        objects:
        - "udp:Udp":
            name: 'udp1'
            sourcePort: '1024'
        - RangeModifier:
            name: 'rangemodifier 1'
            OffsetReference: udp1.destPort
            ModifierMode: INCR
            data: '50000'
            RecycleCount: 8000
            StepValue: 1
            Mask: 65535
         - TableModifier:
            name: 'tablemodifier 1'
            OffsetReference: udp1.sourcePort
            data: '1025 1024'

  4. To create a stream block with multiple source and destination target references,
     need to use the ansible feature jinja2 templeting in yaml. 
     See `Templating jinja2 <https://docs.ansible.com/ansible/latest/user_guide/playbooks_templating.rst#playbooks-templating>`_.

  .. code-block:: yaml
  
    - 
    name: Create a stream block with multiple source and destination targets
    stc: 
        action: create
        under: ref:/Port[@name='Port1']
        objects: 
        - streamblock: 
            TrafficPattern: PAIR
            EnableBidirectionalTraffic: false
            EnableStreamOnlyGeneration: true
            SrcBinding-targets: ref:/EmulatedDevice[@tag='Port1Device']/Ipv4If
            DstBinding-targets: |-
            "{%- for x in range(0, 10) -%}
            ref:/EmulatedDevice[@Name='Port2Dev1']/Ipv4If,
            {%- endfor -%}"
            AffiliationStreamBlockLoadProfile:
            Load: 10
  
Configure Stream Block
----------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing stream block and it's sub object properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure stream block
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         objects: <stream block name reference>  :mandatory:`M`
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
          <div>Specifies the number of stream blocks to be configured.</div>
          <div>Count value above 1, creates several stream block objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in stream block names. The item will be replace 
           with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>xpath</td>
       <td>
            <div>A stream block object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>object: /Port[@Name='Port1']/Streamblock[@Name='Streamblock1']</code></div>
                   or
                   <div><code>object: /project/Streamblock[@Name='Streamblock1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. Stream block must already exist.</div>
                  <div>   2. If the stream block does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of stream block object.</div>
          <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>properties:</code></div>
                   <div><code>FrameLengthMode: "FIXED"</code></div>
                   <div><code>FixedFrameLength: 256</code></div>
            <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/StreamBlock.htm'> StreamBlock object reference guide</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

  .. code-block:: yaml

    - 
      name: Configure a stream block
      stc: 
        action: config
        objects: ref:/Port[@Name='Port1']/Streamblock[@Name='Streamblock1']
        properties:
            FrameLengthMode: "FIXED"
            FixedFrameLength: 256
            AffiliationStreamBlockLoadProfile:
              Load: 100

Start/Stop Traffic(Generator)
-----------------------------

Purpose
~~~~~~~

Starts/stops the  traffic generator. All the active stream blocks in the generator will be started.


Synopsis
~~~~~~~~

.. parsed-literal::

   -
     name: start devices
     stc: 
       action: perform  :mandatory:`M`
       command: GeneratorStart/GeneratorStop  :mandatory:`M`
       properties:
          GeneratorList: <generator object reference>

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
       <td>Specifies the action for the given task. Here it is <code>perform</code>.
         <div><b>Required:</b> Yes.</div>
       </td>
     </tr>
     <tr>
       <td>command   </td>
       <td>string   </td>
       <td>
          <div>Specifies the command name to start/stop the traffic.</div>
          <div>To start traffic, use <code>GeneratorStartCommand</code></div>
          <div>To stop traffic, use <code>GeneratorStopCommand</code></div>
          <div><b>Required:</b> Yes.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
            <div>Specifies the properties supported to perform generatorstart or generatorstop command.
             Currently, supported property is "GeneratorList".</div>
            <div><b>Required:</b> No. Optional field.</div>
            <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/GeneratorStartCommand.htm'> GeneratorStartCommand page</a><div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/GeneratorStopCommand.htm'> GeneratorStopCommand page</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

   # To start traffic on all stream blocks
   -
     name: start traffic
     stc: 
       action: perform  
       command: GeneratorStart

   # To start a specific generator
   -
     name: start traffic
     stc: 
       action: perform
       command: GeneratorStart
       properties:
          GeneratorList: ref:/project

.. code-block:: yaml

   # To stop traffic on all stream blocks
   -
     name: stop traffic
     stc: 
       action: perform  
       command: GeneratorStop

   # To stop a specific generator
   -
     name: stop traffic
     stc: 
       action: perform
       command: GeneratorStop
       properties:
          GeneratorList: ref:/project