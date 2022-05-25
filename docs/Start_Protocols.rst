Start Device (Protocols)
========================

.. contents::
   :local:
   :depth: 1
   
.. role:: mandatory

Purpose
~~~~~~~

Starts all the protocols on the specified device(s) or Port(s).

Synopsis
~~~~~~~~

.. parsed-literal::

   -
     name: start devices
     stc: 
       action: perform :mandatory:`M`
       command: DeviceStart :mandatory:`M`
       properties:
          DeviceList: <Device object reference path>

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
       <td>Specifies the action for the given task. Here it is <code>perform</code>.
         <div><b>Required:</b> Yes.</div>
       </td>
     </tr>
     <tr>
       <td>command   </td>
       <td>string   </td>
       <td>
          <div>Specifies the command name to start the devices.</div>
          <div><b>Required:</b> Yes.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
            <div>Specifies the properties supported to perform devicestart command.
             Currently, supported property is "DeviceList".</div>
            <div><b>Required:</b> No. Optional field.</div>
       </td>
     </tr>
   </table>
   
   </body>
   </html>

Examples
~~~~~~~~

.. code-block:: yaml

   # To start all devices
   -
     name: start devices
     stc: 
       action: perform  
       command: DeviceStart

   # To start a specific device
   -
     name: start devices
     stc: 
       action: perform
       command: DeviceStart
       properties:
          DeviceList: ref:/EmulatedDevice[@Name='Device1']

   # To start devices on a specific port
   -
     name: start devices
     stc: 
       action: perform
       command: DeviceStart
       properties:
          DeviceList: ref:/Port[@Name='Port1']
