Delete Objects
==============

.. contents::
   :local:
   :depth: 1

Purpose
-------

Deletes a specific stc datamodel object(s).
This will also delete all child objects of the deleted objects.

.. role:: mandatory

Synopsis
--------

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::

   -
     name: delete object
     stc: 
       action: delete  :mandatory:`M`
       objects: <object path>  :mandatory:`M`

Parameters
----------

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
       <td>Specifies the action for the given task. 
        Here, it is <code>delete</code>.
          <div><b>Required:</b> Yes.</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>xpath</td>
       <td>
            <div>Specifies the object (port/device/result) path to delete.</div>
            <div><b>Required:</b> Yes.</div>
            <div><b>Example:</b> <code>ref:/EmulatedDevice[@Name='Device1']</code></div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
--------

.. code-block:: yaml

   # To delete Port
   - 
     name: Delete port1
     stc: 
       action: delete
       objects: ref:/port[@name='Port1']

   # To delete a BGP device
   - 
     name: Delete BGP object
     stc: 
       action: delete
       objects: ref:/EmulatedDevice[@Name='Device1']/BgpRouterConfig[@Name='BGPDevice1']

   # To delete an emulated device
   - 
     name: Delete BGP object
     stc: 
       action: delete
       objects: ref:/EmulatedDevice[@Name='Device1']