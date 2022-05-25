Port
====

.. contents::
   :local:
   :depth: 1

Overview
--------

In `STC Ansible`, after creating a session and connecting to the Spirent Test Center chassis, 
you need to create the port objects.

You can create a single or multiple ports. Use `Port` object to create ports under the project.
All the characteristics of a port can be configured during the creation of port itself. 
Same can also be reconfigured/modify later.

Once the port creation is done, you can create/configure the `Emulated Devices <../docs/EmulatedDevice.rst>`_, 
`Stream Blocks <../docs/Stream Block.rst>`_ under the ports.

Then reserve the ports to perform the test and get the expected results.


Create Port
-----------

Purpose
~~~~~~~

Creates port object(s) in the Spirent Test Center(stc) datamodel under the project.
During the object creation, requires to configure it's characteristics like name and location.
The name of the port object will be used as a reference in order to reconfigure/modify
any of it's properties later.


.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.


.. parsed-literal::
   
   -
      name: create port
      stc: 
         action: create  :mandatory:`M`
         under: <project or port object reference> :mandatory:`M`
         count: <integer>
         under: <project reference>  :mandatory:`M`
         objects: 
            - <port object name>  :mandatory:`M`
                <port attribute1: value1>
                <port attribute2: value2>
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
            <div>A project reference under which a stream block is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>under: ref:/project</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='../docs/Session.rst'>Session section</a></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. Session must already exist.</div>
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of stream blocks to be created.</div>
          <div>Count value above 1, creates several port objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in port object names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create port, use <code>Port</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Port.htm'> Port object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

  1. Sample YAML code to create a port under project:
  
  .. code-block:: yaml

    - 
      name: Create a port
      stc: 
        action: create
        under: ref:/project
        objects: 
          - port:
              location: "//10.109.123.122/1/1"
              name: Port1

  2. Sample YAML code to create multiple ports:
  
  .. code-block:: yaml

    - 
      name: Create 10 ports
      stc: 
        action: create
        under: ref:/project
        count: 10
        objects: 
          - port:
              location: "//10.109.123.122/1/$item"
              name: Port-$item

  3. Create ports with the reference to pre-defined port locations and names.
     Chassis, ports and names will be defined in session creation task or in an inventory.ini file.
     Please refer `Session <../docs/Session.rst>`_ section for more details.

  .. code-block:: yaml

    - 
      name: Create 10 ports
      stc: 
        action: create
        under: ref:/project
        count: 10
        objects: 
          - port:
              location: "//${chassis[0]}/1/$item"
              name: Port-$item

    -
      name: Create 11 ports
      stc:
        action: create
        count: 11
        under: ref:/project
        objects:
           - port:
               location: ${ports[item]}
               name: ${names[item]}

  4. Sample YAML code to create offline ports:
  
  .. code-block:: yaml

    - 
      name: Create a port
      stc: 
        action: create
        under: ref:/project
        objects: 
          - port:
              location: "//(Offline)/1/1"
              name: Port1
          - port:
              location: "//(Offline)/1/2"
              name: Port2

Configure Port
--------------

Purpose
~~~~~~~

Reconfigures/modifies an existing port properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure port
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         objects: <port name reference>  :mandatory:`M`
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
          <div>Specifies the number of ports to be configured.</div>
          <div>Count value above 1, creates several port objects in an iterative way. </div>
          <div>Use the keyword ${item} as a template in port names. The item will be replace 
           with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>xpath</td>
       <td>
            <div>A port object under which the attributes are configured.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>object: /Port[@Name='Port1']</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. Session must already exist.</div>
                  <div>   2. If the port does not exist with the specified name, an exception will be raised and the playbook stops.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of port object.</div>
          <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>properties:</code></div>
                   <div><code>location: "//10.109.123.12/1/1"</code></div>
            <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Port.htm'> Port object reference guide</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

  .. code-block:: yaml

    - 
      name: Configure port properties
      stc: 
        action: config
        under: ref:/project
        objects: ref:/Port[@Name='Port1']
        properties:
            location: "//10.109.123.123/1/1"


Bring ports online/offline
--------------------------

Purpose
~~~~~~~

Reserves/releases and map/unmap one or more ports.


Synopsis
~~~~~~~~

.. parsed-literal::

   -
     name: Reserve/Release ports
     stc: 
       action: perform  :mandatory:`M`
       command: Attachports/DetachPorts  :mandatory:`M`
       properties:
          PortList: <port object reference>

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
          <div>Specifies the command name to reserve or release ports.</div>
          <div>To reserve ports, use <code>AttachportsCommand</code></div>
          <div>To release ports, use <code>DetachPortsCommand</code></div>
          <div><b>Required:</b> Yes.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
            <div>Specifies the properties supported to perform AttachPorts or DetachPorts command.
            <div><b>Required:</b> Yes.</div>
            <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/AttachPortsCommand.htm'> AttachPortsCommand page</a><div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/DetachPortsCommand.htm'> DetachPortsCommand page</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

   # To reserve one port
   -
     name: Take ports online
     stc: 
       action: perform  
       command: AttachPorts
       properties:
          PortList: ref:/port[@Name='Port1']

   # To reserve all ports
   -
     name: Take ports online
     stc: 
       action: perform  
       command: AttachPorts
       properties:
          PortList: ref:/port

   # To release one port
   -
     name: Take ports offline
     stc: 
       action: perform  
       command: DetachPorts
       properties:
          PortList: ref:/port[@Name='Port1']

   # To release ports
   -
     name: Take ports offline
     stc: 
       action: perform
       command: DetachPorts
       properties:
          PortList: ref:/port
