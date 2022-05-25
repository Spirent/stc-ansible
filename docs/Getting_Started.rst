Getting Started
===============


.. contents::
   :local:
   :depth: 1
   
Introduction
------------

STC Ansible is an experimental plugin designed to configure Spirent TestCenter data models
and execute tests.


Preparation
-----------

- This STC Ansible module requires a recent version (>=2.5) of the Ansible client.
- This STC Ansible module can be used to remote configure an STC Lab Server.
- Configuration of STC-web is currently not supported.
- This module is supported and tested in Linux (Ubuntu 18.04 64bit) environment.

Installation
------------

First, you need to install Python dependencies for the Ansible client:

.. parsed-literal::
    `pip install ansible`
    `pip install requests`
    `pip install pytest`

Configuration
-------------

Inventory
~~~~~~~~~

In your inventory (inventory.ini), declare the STC Lab Servers you want the Ansible playbook to connect to:

.. parsed-literal::

    [labservers]
    my-labserver-1 ansible_host=10.61.67.200

    [labservers:vars]
    ansible_connection=paramiko
    ansible_host_key_checking=no
    ansible_user=admin
    ansible_ssh_pass=spirent
    ansible_ssh_common_args=/bin/ssh
    ansible_paramiko_pty=no

.. note:: `ansible_paramiko_pty` must be set to no as it will otherwise fail to connect to the STC Lab Server.

Ansible STC Module
~~~~~~~~~~~~~~~~~~

If you want to use the STC module outside of this direction, you will need to copy the content 
of the `module_utils` and `library` into the folder from which you are running your Ansible playbook.

Running an Ansible Playbook
---------------------------

There are several example playbooks in the `playbooks <https://github.com/Spirent/stc-ansible/tree/master/playbooks>`_ folder. To run all of them, 
just use make play, and it will create an STC session for each of the playbooks. 
(You can also use make debug to run ansible with extra verbose output).

Debugging
~~~~~~~~~

Debugging can be difficult when using Ansible. 
To make it easier to troubleshoot your playbook, you can use the STC ansible emulator. For example:

.. parsed-literal::

    ./emulator.py -labserver lab-serverIP-address you-playbook.yaml

STC Ansible Actions
-------------------

The stc Ansible module makes it possible to execute one of the following actions:

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
       <th style="text-align: center">action</th>
       <th style="text-align: center">Description</th>
     </tr>
     <tr>
       <td>create_session or session</td>
       <td>
           <div>Attach to an existing session. If the session does not exsit, a new session is created.</div>
           <div>If the session exists, the data model is first reset to the default data model.</div>
       </td>
     </tr>
     <tr>
       <td>attach_session</td>
       <td>
           <div>Attach to an existing session. If the session does not exisit, the script will fail.</div>
       </td>
     </tr>
     <tr>
       <td>delete_session</td>
       <td>
           <div>Deletes a specific session or few sessions specified.</div>
       </td>
     </tr>
     <tr>
       <td>delete_all_sessions</td>
       <td>
           <div>Deletes all the existing sessions.</div>
       </td>
     </tr>
     <tr>
       <td>load</td>
       <td>
           <div>Loads a predefined XML data model. Note that the model must first be copied to the target</div>
           <div>STC Lab Server using the copy module. Check the datamodel-loader.yaml playbook for reference.</div>
       </td>
     </tr>
     <tr>
       <td>create</td>
       <td>
           <div>Creates a new object in the data model.</div>
       </td>
     </tr>
     <tr>
       <td>config</td>
       <td>
           <div>Configures an existing object in the data model.</div>
       </td>
     </tr>
     <tr>
       <td>perform</td>
       <td>
           <div>Perform a command against the data model.</div>
       </td>
     </tr>
     <tr>
       <td>delete</td>
       <td>
           <div>Deletes an object in the data model.</div>
       </td>
     </tr>
     <tr>
       <td>get</td>
       <td>
           <div>Returns the value of a given attribute of one or more objects -</div>
           <div>this can be used for instance to check results.</div>
       </td>
     </tr>
     <tr>
       <td>wait</td>
       <td>
           <div>Waits for one of several object attribute to become a specific value </div>
           <div>(eg wait for the attritube BlockState of the PPPoE object PppoeClientBlockConfig to become CONNECTING )</div>
       </td>
     </tr>
     <tr>
       <td>download</td>
       <td>
           <div>Download files such as bll.log, bll.session.log, etc...</div>
       </td>
     </tr>
   </table>

   </body>
   </html>

STC configuration structure
---------------------------

The STC Ansible module does not connect directly to the STC Lab Server via the STC REST API. 
Instead, it first ssh into the STC Lab Server, and then uses the REST API to connect to the BLL.

.. image:: /docs/_static/images/design.png


Related Documentation
~~~~~~~~~~~~~~~~~~~~~

Additional documentation related to this guide:

- `Instructions on how to set up LabServer` - https://support.spirent.com/SpirentCSC/SC_KnowledgeView?cid=null&id=DOC10792

- `Spirent TestCenter Automation Object Reference` - http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/index-all.htm

- `Ansible user guide` - https://docs.ansible.com/ansible/latest/user_guide/index.html

- `YAML syntax` - https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html


