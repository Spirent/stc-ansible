System
======

.. contents::
   :local:
   :depth: 1

Overview
--------

After creating a session, STC ansible allows to configure License Server host details which 
requires to reserve Spirent TestCenter virtual ports.

Also, if declaring your own data model is too complex, you can import/load an 
existing XML data model.
You must first copy the data model to the STC Lab Server before you are able to import/load it.

Configure License Server
------------------------

Purpose
~~~~~~~

Configures the License server (virtual controller) that hosts port and feature license files. 
License servers are only required when reserving Spirent TestCenter virtual ports.


.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.


.. parsed-literal::
   
    -
      name: Configure the lab server license manager
      stc: 
        action: create     :mandatory:`M`
        under: /system/LicenseServerManager    :mandatory:`M`
        objects:
        - LicenseServer:       :mandatory:`M`
            <propertyname>: <value>   

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
            <div>A licenseserver manager path which is automatically created object of a test hierarchy.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>under: /system/LicenseServerManager</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='../docs/Session.rst'>Session section</a></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
                <div><b>NOTES:</b></div>
                  <div>   1. Session must already exist.</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>string</td>
       <td>
          <div>Specifies to identify stc objects and attributes.</div>
          <div>To configure license server properties, use <code>LicenseServer</code> object.</div>
          <div><b>Required:</b> Yes.</div>
            <div><b>Example:</b></div>
                   <div><code>objects: </code></div>
                   <div><code>- LicenseServer: </code></div>
                   <div><code>Server: 127.0.0.1</code></div>
          <div><b>See Also:</b></div>
          <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/LicenseServer.htm'> LicenseServer object reference guide</a><div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

  Sample YAML code to configure primary and backup License servers:
  
  .. code-block:: yaml

    -
      name: Configure the lab server license manager
      stc: 
        action: create
        under: /system/LicenseServerManager
        objects:
          - LicenseServer:
              Server: 10.66.240.120
              BackupServer: 10.66.240.130
              Name: LicenceServer


Load Data Module
----------------

To copy an existing XML data model to the STC Lab Server, use the following YAML code 
by providing source and destination paths.


  .. code-block:: yaml

    -
      name: Copy the data model
      copy:
        src: asset/datamodel.xml
        dest: /tmp/datamodel.xml

Load/import the XML datamodel to the STC Lab Server, use the following YAML task by specifying
the action as `load` and datamodel path.


  .. code-block:: yaml


    - name: Load a data model
      stc:
        action: load
        datamodel: /tmp/datamodel.xml



