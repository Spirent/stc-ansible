Multicast Group
===============

.. contents::
   :local:
   :depth: 1

Overview
--------

In `STC Ansible` you can create IPv4 or IPv6 multicast group objects.

These multicast group objects will be used for the IGMP (for IPv4), MLD (for IPv6), and PIM protocols.

Create Multicast Group
----------------------

Purpose
~~~~~~~

Creates IPv4 or IPv6 multicast group object(s) in the Spirent Test Center(stc) datamodel under the project.
During the object creation, Name and other properties can be defined.
The name of the multicast group will be used as a reference in order to reconfigure/modify
any of it's properties later.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: create multicast group
      stc: 
         action: create  :mandatory:`M`
         under: <project reference> :mandatory:`M`
         count: <integer>
         objects: 
            - <multicast group object name>  :mandatory:`M`
              <multicast attribute1: value1>
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
            <div>A project under which the multicast group is created.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>under: ref:/project</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
       </td>
     </tr>
     <tr>
       <td>count   </td>
       <td>integer   </td>
       <td>
          <div>Specifies the number of multicast groups to be created.</div>
          <div>Count value above 1, creates several multicast groups in an iterative way. </div>
          <div>Use the keyword ${item} as a template in group names. The item will be replace with the values from 1 to count.</div>
          <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To create IPv4 multicast group, use <code>Ipv4group</code> object.</div>
          <div>To create IPv6 multicast group, use <code>Ipv6group</code> object.</div>
          <div><b>Required:</b> Yes.</div>
          <div><b>See Also:</b></div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ipv4Group.htm'> IPv4 Multicast group reference guide</a><div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ipv6Group.htm'> IPv6 Multicast group reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: create IPv4 Multicast group
      stc: 
        action: create
        under: /project
        count: 1
        objects: 
          - Ipv4group: 
             name: Ipv4Group1
             Active: true
             Ipv4NetworkBlock:
                StartIpList: 225.0.0.1
                PrefixLength: 32
                NetworkCount: 10
                Active: true

    -
      name: create IPv6 Multicast group
      stc: 
        action: create
        under: /project
        count: 1
        objects: 
          - Ipv6group: 
             name: Ipv6Group1
             Active: true
             Ipv6NetworkBlock:
                StartIpList: ff1e::1
                PrefixLength: 128
                NetworkCount: 10
                Active: true

    -
      name: create 10 IPv4 multicast groups
      stc: 
         action: create
         under: /project
         count: 10
         objects: 
            -IPv4group
               Name: "Ipv4group${item}"
               Active: true
               Ipv4NetworkBlock:
                  StartIpList: 225.0.${item}.1
                  PrefixLength: 32
                  NetworkCount: 10
                  Active: true



Configure Multicast Group
-------------------------

Purpose
~~~~~~~

Reconfigures/modifies an existing multicast group properties.

.. role:: mandatory


Synopsis
~~~~~~~~

.. parsed-literal::
   -
      name: configure multicast group
      count: <integer>
      stc: 
         action: config  :mandatory:`M`
         object: <project reference>  :mandatory:`M`
         properties:   :mandatory:`M`
            <multicast group attribute1: value1>
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
          <div>Specifies the number of multicast groups to be configured.</div>
          <div>Count value above 1, configures several multicast groups in an iterative way. </div>
          <div>Use the keyword ${item} as a template in group names. The item will be replace 
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
                   <div><code>object: ref:/project</code></div>
                   <div>OR</div>
                   <div><code>object: /project</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
          <div>Specifies to identify the properties of multicast group.</div>
          <div><b>Required:</b> Yes</div>
          <div>For IPv4 multicast group attributes, please refer <div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ipv4Group.htm'> IPv4 multicast group reference guide</a><div>
          <div>For IPv6 multicast group attributes, please refer <div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/Ipv6Group.htm'> IPv6 multicast group reference guide</a><div>
       </td>
     </tr>
   </table>


Examples
~~~~~~~~

.. code-block:: yaml

    -
      name: configure IPv4 multicast group
      stc: 
      action: config
      count: 1
      object: ref:/project/Ipv4Group[@Name='Ipv4group1']
      properties: 
         Ipv4NetworkBlock:
            StartIpList: 225.0.1.1
            PrefixLength: 32
            NetworkCount: 10
            Active: true

    -
      name: configure IPv6 multicast group
      stc: 
      action: config
      count: 1
      object: ref:/project/Ipv6Group[@Name='Ipv6group1']
      properties: 
         Ipv6NetworkBlock:
            StartIpList: ff1e::1
            PrefixLength: 128
            NetworkCount: 10
            Active: true

