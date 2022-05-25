Results
=======

.. contents::
   :local:
   :depth: 1

Overview
--------

STC Ansible allows you to subscribe to a runtime Result Views (Classic views) that is already 
defined by a Result View Template XML file.

After completing the test configuration, you need to subscribe specific result views in order
to get and display the results related to your current test.

In STC Ansible to get DRV results, first you need to create Dynamic Result View by defining 
the required properties and then need to subscribe them.

After subscribing the result views, you can start the test (Start devices/traffic) and get the 
results. Using `register` option, you can store the result output in a variable. To display the
stored result content you need to use `debug` task.

Subscribe Results
-----------------

Purpose
~~~~~~~

Specifies to subscribe to a runtime Result View that is already defined by a Result
View Template XML file.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.


.. parsed-literal::
   
   -
     name: subscribe results
     stc: 
       action: perform  :mandatory:`M`
       command: SubscribeResultsView  :mandatory:`M`
       properties: 
          TemplateUri: <result view template xml>  :mandatory:`M`


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
           <div>Specifies the action for the given task. Here, it is <code>perform</code>.</div>
           <div><b>Required:</b> Yes</div>
       </td>
     </tr>
     <tr>
       <td>command</td>
       <td>string</td>
       <td>
          <div>Specifies the command name to subscribe the result views.</div>
          <div>To subscribe result views, use <code>SubscribeResultsView</code> command.</div>
          <div><b>Required:</b> Yes.</div>
       </td>
     </tr>
     <tr>
       <td>properties</td>
       <td>string</td>
       <td>
            <div>Specifies the properties supported to perform subscribe results command.
            <div><b>Required:</b> Yes.</div>
            <div><b>Example:</b> </div>
            <div><code>properties:</code></div>
            <div><code>TemplateUri: "/Result Views/Stream Results/Stream Block Results.xml"</code></div>
            <div><b>See Also:</b></div>
            <div>    <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/SubscribeResultsViewCommand.htm'> SubscribeResultsViewCommand page</a><div>
            <div><b>NOTES:</b></div>
            <div>Default result view template xml files are available in Labserver under</div>
            <div>"/home/testcenter/server/Templates/System/Result Views/"</div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

  1. Sample YAML code to subscribe Stream Block Results:
  
  .. code-block:: yaml

    - 
      name: subscribe to streamblock results
      stc: 
        action: perform
        command: SubscribeResultsView
        properties: 
          ExecuteSynchronous: true
          TemplateUri: "/Result Views/Stream Results/Stream Block Results.xml"

  2. Sample YAML code to subscribe Detailed Stream Results:
  
  .. code-block:: yaml

    - 
      name: subscribe to streamblock results
      stc: 
        action: perform
        command: SubscribeResultsView
        properties: 
          ExecuteSynchronous: true
          TemplateUri: "/Result Views/Stream Results/Detailed Stream Results.xml"

  3. Sample YAML code to subscribe PPPox Results:
  
  .. code-block:: yaml

    - 
      name: subscribe to PPPoX results
      stc: 
        action: perform
        command: SubscribeResultsView
        properties: 
          ExecuteSynchronous: true
          TemplateUri: "/Result Views/Access Protocols/PPPoX Results.xml"



Get results
-----------

Purpose
~~~~~~~

Specifies to get the results from the properties of the result object defined in the data model.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.


.. parsed-literal::
   
   -
     name: get results
     register: <string>
     stc: 
       action: get  :mandatory:`M`
       objects: <result object path>  :mandatory:`M`

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
       <td>register</td>
       <td>string</td>
       <td>
           <div>Specifies a variable name to store the results. </div>
           <div>It will be used later to display the received result counters details.</div>
           <div><b>Required:</b> No. optional field.</div>
       </td>
     </tr>
     <tr>
       <td>action</td>
       <td>string</td>
       <td>
           <div>Specifies the action for the given task. Here, it is <code>get</code>.</div>
           <div><b>Required:</b> Yes</div>
       </td>
     </tr>
     <tr>
       <td>command</td>
       <td>string</td>
       <td>
          <div>Specifies the command name to subscribe the result views.</div>
          <div>To subscribe result views, use <code>SubscribeResultsView</code> command.</div>
          <div><b>Required:</b> Yes.</div>
       </td>
     </tr>
     <tr>
       <td>objects</td>
       <td>xpath</td>
       <td>
          <div>Specifies to identify result object names.</div>
            <div><b>Required:</b> Yes</div>
            <div><b>Example:</b></div>
                   <div><code>objects: /port/StreamBlock/RxStreamBlockResults</code></div>
                   <div><code>objects: /port/StreamBlock/TxStreamBlockResults</code></div>
                   <div><code>objects: /EmulatedDevice[@Name='PPPoE']/PppoeServerBlockConfig/</code></div>
                   <div><code>PppoeServerBlockResults</code></div>
            <div><b>See Also:</b></div>
                   <div> - <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/index-result.htm'> Result object reference guide</a></div>
                   <div> - <a href='https://www.w3schools.com/xml/xpath_syntax.asp'>XPATH Standard (Selecting Nodes)</a></div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

  1. Sample YAML code to get StreamBlock Rx Results:
  
  .. code-block:: yaml

    - 
      name: get StreamBlock Rx Results
      register: resultRx
      stc: 
        action: get
        objects: /port/StreamBlock/RxStreamBlockResults

  2. Sample YAML code to get StreamBlock Tx Results:
  
  .. code-block:: yaml

    - 
      name: get StreamBlock Tx Results
      register: resultRx
      stc: 
        action: get
        objects: /port/StreamBlock/TxStreamBlockResults

  3. Sample YAML code to get PPPoE Server Results:
  
  .. code-block:: yaml

    - 
      name: Get the server binding results
      register: pppoxresult
      stc: 
        action: get
        objects: /EmulatedDevice[@Name='PPPoE Server']/PppoeServerBlockConfig/PppoeServerBlockResults

Display Results
---------------

To display the results or the output of the registered variable, use the debug task.

.. parsed-literal::
   
    - debug:
        var: <result variable name>

Examples
~~~~~~~~

  1. Sample YAML code to get and display the StreamBlock Rx Results:
  
  .. code-block:: 
  
    -
      name: get StreamBlock Rx Results
      register: resultRx
      stc: 
        action: get
        objects: /port/StreamBlock/RxStreamBlockResultss

    - debug:
        var: resultRx


Create and get DRV Results
--------------------------

Purpose
~~~~~~~

Creates the dynamic result view (DRV) related queries and properties. The sub object 
`PresentationResultQuery` provides SQL like syntax for defining the result that users 
are interested in.
After creating the DRV query, subscribes and get the DRV specific result counters.

.. role:: mandatory


Synopsis
~~~~~~~~

.. note:: :mandatory:`M` indicates that the parameter is  :mandatory:`Mandatory`.

.. parsed-literal::
   -
      name: create a DRV
      stc: 
         action: create  :mandatory:`M`
         under: <project reference> :mandatory:`M`
         objects: 
            - DynamicResultView:  :mandatory:`M`
                PresentationResultQuery:  :mandatory:`M`
                <DRV attribute1: value1>
                <DRV attribute2: value2>
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
            <div>A project reference under which the Dynamic Result View is created.</div>
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
          <div>To create a DRV, use <code>DynamicResultView</code> object.</div>
          <div><b>Required:</b> Yes.</div>
            <div><b>Example:</b></div>
                   <div><code>objects: </code></div>
                   <div><code>-DynamicResultView: </code></div>
                   <div><code>  PresentationResultQuery: </code></div>
                   <div><code>  Selectproperties: "StreamBlock.StreamId StreamBlock.Name Port.Name" </code></div>
          <div><b>See Also:</b></div>
          <div> <a href='http://kms.spirentcom.com/CSC/pabtech/stc-automation-html/DynamicResultView.htm'> DynamicResultView object reference guide</a><div>
          <div><b>NOTES:</b></div>
            <div> If the DRV query parameters are not valid, the create action will not fail, but the subsequent drv.subscribe will fail.</div>
       </td>
     </tr>
   </table>

   </body>
   </html>


Examples
~~~~~~~~

.. code-block:: yaml

    - 
    name: Create a DRV for dropped frames
    stc: 
        action: create
        under: ref:/project
        objects:
        - DynamicResultView:
            name: "Dropped Frames DRV" 
            PresentationResultQuery:
                DisableAutoGrouping: True
                SelectProperties: "StreamBlock.StreamId StreamBlock.Name Port.Name StreamBlock.ActualRxPortName StreamBlock.FrameConfig.ipv4:IPv4.1.sourceAddr StreamBlock.FrameConfig.ipv4:IPv4.1.destAddr StreamBlock.FrameConfig.ethernet:EthernetII.1.srcMac StreamBlock.FrameConfig.ethernet:EthernetII.vlans.Vlan.1.id StreamBlock.TxFrameCount StreamBlock.RxSigFrameCount StreamBlock.TxFrameRate StreamBlock.RxSigFrameRate StreamBlock.DuplicateFrameCount StreamBlock.DroppedFrameCount StreamBlock.DroppedFrameDuration StreamBlock.MinLatency StreamBlock.MaxLatency StreamBlock.AvgLatency StreamBlock.IsExpected"
                WhereConditions: "{StreamBlock.DroppedFrameCount > 0 AND StreamBlock.IsExpected = 1}"
                SortBy: "{StreamBlock.DroppedFrameCount DESC}"
                FromObjects: ref:/project/port
                LimitSize: 20000


Subscribe DRV Results
~~~~~~~~~~~~~~~~~~~~~

To subscribe the DRV results use the following YAML task.

  .. code-block:: yaml

    -
      name: Subscribe DRV results for dropped frames
      stc: 
        action: drv.subscribe
        objects: ref:/project/DynamicResultView[name="Dropped Frames DRV"] 

Get and display DRV Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get and display the DRV results use the following YAML task.

  .. code-block:: yaml

    -
      name: Fetch DRV results for dropped frames
      register: DRVResults
      stc: 
        action: drv.fetch
        objects: ref:/project/DynamicResultView[name="Dropped Frames DRV"] 

    - 
      debug:
        var: DRVResults
