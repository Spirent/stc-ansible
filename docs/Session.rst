Session
=======

.. contents::
   :local:
   :depth: 1

Overview
--------

In `STC Ansible`, the first task of the playbook must be to create/attach to a STC labserver session.

To create new session, you need to use `session` or `create_session` actions by specifing the user 
and session name. If the session is already exists with the given name, it will attach automatically.

If you wanted to connect only to an existing session, then use `attach_session` action.

`STC Ansible` also allows to delete the existing sessions using `delete_session` and `delete_all_sessions`.


Create Session
--------------

Purpose
~~~~~~~

Creates session or attaches to an exisiting session.


.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.


.. parsed-literal::
   
   -
      name: create session
      stc: 
         action: session or create_session    :mandatory:`M`
         user: <session user name>   :mandatory:`M`
         name: <session name>   :mandatory:`M`
         kill_existing: <true|false>
         reset_existing: <true|false>
         chassis: <chassis ip list>
         ports: <slot/ports location list>
         names: <port names>

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
           <div>Specifies the action for the given task. Here, it is <code>session</code> or <code>create_session</code>.</div>
           <div><b>Required:</b> Yes</div>
       </td>
     </tr>
     <tr>
       <td>user</td>
       <td>string</td>
       <td>
           <div> Specifies the STC labserver session user name. </div>
           <div><b>Required:</b> Yes</div>
       </td>
     </tr>
     <tr>
       <td>name</td>
       <td>string</td>
       <td>
           <div> Specifies the STC labserver session name. </div>
           <div><b>Required:</b> Yes</div>
       </td>
     </tr>
     <tr>
       <td>kill_existing</td>
       <td>choice
          <div>true/false</div>
       </td>
       <td>
          <div>Specifies to kill/attach to the existing session.</div>
          <div>When the value is set to true - If the session with the given name is already exists on the connected STC lab server, it will be first killed and then creates new session./div>
          <div>When the value is set to false - Attaches to an existing session./div>
          <div>Default value is false.</div>
          <div><b>Required:</b> No. Optional field.</div>
       </td>
     </tr>
     <tr>
       <td>reset_existing</td>
       <td>choice
          <div>true/false</div>
       </td>
       <td>
          <div>Specifies to reset the configuration.</div>
          <div>When the value is set to true - Resets the in-memory configuration before connecting to the session./div>
          <div>When the value is set to false - It will not perform reset./div>
          <div>Default value is true.</div>
          <div><b>Required:</b> No. Optional field.</div>
       </td>
     </tr>
     <tr>
       <td>chassis</td>
       <td>string</td>
       <td>
          <div>Specifies the IP or hostname of the chassis to connect to.</div>
          <div><b>Required:</b> No. Optional field.</div>
          <div><b>Example:</b></div>
          <div><code>chassis: "10.109.118.32" </code></div> OR
          <div>If the chassis IPs are already defined in inventory.ini file,</div>
          <div><code>chassis: "{{ hostvars[inventory_hostname].chassis }}" </code></div>
          <div><b>See Also:</b></div>
          <div> - <a href='../docs/Getting_Started.rst'>Getting Started</a> section to configure inventory.ini file</div>
       </td>
     </tr>
     <tr>
       <td>ports</td>
       <td>string</td>
       <td>
          <div>Specifies the location of the slot/ports.</div>
          <div><b>Required:</b> No. Optional field.</div>
          <div><b>Example:</b></div>
          <div><code>ports: //${chassis[0]}/1/1 </code></div>
          <div>If ports are already defined in inventory.ini file,</div>
          <div><code>ports: "{{ hostvars[inventory_hostname].ports }}" </code></div>
          <div><b>See Also:</b></div>
          <div> - <a href='../docs/Getting_Started.rst'>Getting Started</a> section to configure inventory.ini file</div>
       </td>
     </tr>
     <tr>
       <td>names</td>
       <td>string</td>
       <td>
          <div>Specifies to define the port names.</div>
          <div><b>Required:</b> No. Optional field.</div>
          <div>Example:</div>
          <div><code>names: Port-1, Port-2 </code></div>
          <div>If port names are already defined in inventory.ini file,</div>
          <div><code>names: "{{ hostvars[inventory_hostname].names }}" </code></div>
          <div><b>See Also:</b></div>
          <div> - <a href='../docs/Getting_Started.rst'>Getting Started</a> section to configure inventory.ini file</div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

  1. Sample YAML code to create a session:
  
  .. code-block:: yaml

    - 
      name: Create a session
      stc: 
        action: session
        user: ansible
        name: sample_session1
        chassis: "10.109.118.32"

   OR
   
    - 
      name: Create a session
      stc: 
        action: create_session
        user: ansible
        name: sample_session1
        chassis: "10.109.118.32"

  2. Sample YAML code to create a session with pre-defined chassis, ports and names in the inventory.ini file:
  
  .. code-block:: yaml

    - 
      name: Create a session
      stc: 
        action: create_session
        user: ansible_user
        name: sample_session1
        chassis: "{{ hostvars[inventory_hostname].chassis }}"
        ports: "{{ hostvars[inventory_hostname].ports }}"
        names: "{{ hostvars[inventory_hostname].names }}"

  3. Sample YAML code to create a session with single chassis,slot and multiple ports:
  
  .. code-block:: yaml

    - 
      name: Create a session
      stc: 
        action: create_session
        user: mkatta
        name: multi-port-test1
        chassis: "10.108.8.10"
        ports: "//${chassis[0]}/2/1-5,6,8 //${chassis[0]}/2/7"
        names: "port[1:7] qmport[8:8]"

    -
      name: Create ports using pre-defined port locations and names
      stc:
        action: create
        count: 8
        objects:
          - project:
               - port:
                  location: ${ports[item]}
                  name: ${names[item]}

  4. Sample YAML code to create a session with single chassis and multiple slots/ports:
  
  .. code-block:: yaml

    - 
      name: Create a session
      stc: 
        action: create_session
        user: mkatta
        name: multi-port-test1
        chassis: "10.109.115.123"
        ports: "//${chassis[0]}/2/1-3,4,5 //${chassis[0]}/9/1"
        names: "port[1:5] [6:6]myport"

    -
      name: Create ports using pre-defined port locations and names
      stc:
        action: create
        count: 6
        objects:
          - project:
               - port:
                  location: ${ports[item]}
                  name: ${names[item]}

  5. Sample YAML code to create a session with multiple chassis and multiple slots/ports:
  
  .. code-block:: yaml

    - 
      name: Create a session
      stc: 
        action: create_session
        user: mkatta
        name: multi-port-test1
        chassis: "10.109.115.123 10.109.112.121"
        ports: "//${chassis[0]}/2/1-3,4,5 //${chassis[1]}/1/1"
        names: "port[1:5] [6:6]myport"

    -
      name: Create ports using pre-defined port locations and names
      stc:
        action: create
        count: 6
        objects:
          - project:
               - port:
                  location: ${ports[item]}
                  name: ${names[item]}

Attach an existing Session
--------------------------

Purpose
~~~~~~~

Use to attach an existing STC labserver session. If the session doen't exist, the playbook will fail.

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.


.. parsed-literal::
   
   -
      name: Attach session
      stc: 
         action: attach_session    :mandatory:`M`
         user: <session user name>
         name: <session name>

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
           <div>Specifies the action for the given task. Here, it is <code>attach_session</code>.</div>
           <div><b>Required:</b> Yes</div>
       </td>
     </tr>
     <tr>
       <td>user</td>
       <td>string</td>
       <td>
           <div> Specifies the STC labserver session user name. </div>
           <div><b>Required:</b> Yes</div>
       </td>
     </tr>
     <tr>
       <td>name</td>
       <td>string</td>
       <td>
           <div> Specifies the STC labserver session name. </div>
           <div><b>Required:</b> Yes</div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

  Sample YAML code to attach a session:
  
  .. code-block:: yaml

    - 
      name: Attach a session
      stc: 
        action: attach_session
        user: ansible
        name: session1



Delete Session
--------------

Purpose
~~~~~~~

Use to delete an existing session/all the sessions.

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.


.. parsed-literal::
   
   -
      name: Delete session
      stc: 
         action: delete_session or delete_all_sessions    :mandatory:`M`
         user: <session user name>
         name: <session name> 

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
           <div>Specifies the action for the given task. Here, it is <code>delete_session</code> or <code>delete_all_sessions</code>.</div>
           <div><b>Required:</b> Yes</div>
       </td>
     </tr>
     <tr>
       <td>user</td>
       <td>string</td>
       <td>
           <div> Specifies the STC labserver session user name.</div> 
           <div> This parameter can be specified when specific user created sessions need to be deleted.</div>
           <div>Applicable only for delete_session action.</div>
           <div><b>Required:</b> No. Optional field</div>
       </td>
     </tr>
     <tr>
       <td>name</td>
       <td>string</td>
       <td>
           <div> Specifies the STC labserver session name or names. </div>
           <div>Applicable only for delete_session action.</div>
           <div><b>Required:</b> Yes</div>
          <div><b>Example:</b></div>
          <div><code>name: Session1</code></div>
          <div>To delete multiple sessions:</div>
          <div><code>name: Session1, Session 2, Session3</code></div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

  1. Sample YAML code to delete a session:
  
  .. code-block:: yaml

    - 
      name: Delete a session
      stc: 
        action: delete_session
        name: session1

  2. Sample YAML code to delete a session created by a specific user:
  
  .. code-block:: yaml

    - 
      name: Delete a session
      stc: 
        action: delete_session
        user: ansible
        name: session1

  3. Sample YAML code to delete multiple sessions created by a specific user:
  
  .. code-block:: yaml

    - 
      name: Delete a session
      stc: 
        action: delete_session
        user: ansible
        name: session1, session2

  4. Sample YAML code to delete all the existing sessions in the connected STC lab server:
  
  .. code-block:: yaml

    - 
      name: Delete a session
      stc: 
        action: delete_all_sessions
