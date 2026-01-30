# QGIS-Feature-Annotation-Toolbar
This QGIS plugin implements a toolbar to quickly and easily create and manage annotated pointfeatures in a dedicated layer. 

<img width="267" height="39" alt="image" src="https://github.com/user-attachments/assets/c09941bd-5f24-4fd4-808c-a1538c066c20" /><br/>  

### Feature Annotation Toolbar
**Overview**  
The Feature Annotation Toolbar is meant to quickly mark features on a map using a simple and intuitive method. Markers can be placed quickly and easily near points-of-interest, and are accompanied by a note which is visible in the marker's label. The markerslayer is a plain pointlayer which can be exported and manipulated by the usual methods, and customized to taste. The process is applicable in many situations, and is easily adaptable to various workflows.  

<img width="917" height="649" alt="image" src="https://github.com/user-attachments/assets/4beff7ed-3961-4f65-98c6-bba88a9835a0" /><br/>  

The plugin also features managementfunctions to group and categorize your workload in batches. You can quickly start a session which generates a dedicated folder with geojson items and includes a simple, accessible logfile. Features can additionally be flagged as active, which locks the features while being assigned to separate groups if necessary. When features are no longer needed, they can be archived.

**Installation**  
Use the plugin manager to install the plugin. Alternatively, you can download a zipfile of the code repository using the Code-button available on this repository's github page.  
See: https://docs.qgis.org/3.40/nl/docs/user_manual/plugins/plugins.html#  
See: https://docs.qgis.org/3.40/nl/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab   

#
### Operation  
The plugin allows two modes of operation. **Ad-hoc**-mode, or **Session**-mode. In **Ad-hoc**-mode, the plugin will create a memory-layer without backing. Markers will simply be added to the layer. If you want to save your work, you should make the layer permanent choosing your preferred storageformat. This mode is useful for quick temporary markers, or storage that does not require logging and archiving.  
In **Session**-mode, the plugin will also create a memory-layer, but at the same time it creates an internal, open backingstore with logging and archiving available. Markers are stored as readable geojson items, logging is available in a csv-file, and the session becomes available in a quick-select menu. In addition, the plugin can identify the layer as a session-layer, so it can rebuild the layer on demand.

### Ad-hoc mode  
The plugin's primary task is extremely simple. Add annotated markers to a map quickly. Because of the ease of application, you can rappidly mark a lot of locations in quick succession. And since it uses a plain pointfeature layer, the result can easily be integrated in further workflows. The potential applications are limitless. You can quickly mark errors, mutations, or any other points-of-interest, and label the situation or desired corrections accordingly.  

<img width="107" height="39" alt="image" src="https://github.com/user-attachments/assets/a6177028-692e-4b40-9eeb-794e6a017152" />  

The **Ad-hoc**-mode only requires the first three token-buttons. The buttons represent **Add, Modify,** and **Remove**. The buttons do exactly as indicated. To start the process, simply click the **Add** button. This will start a marker MapTool. You can then click the map and mark a location to add a pointfeature with label. As soon as you click a location, the plugin will first ask for a comment.  

<img width="360" height="332" alt="image" src="https://github.com/user-attachments/assets/ad8a6b65-7da3-4414-b6ff-5b87cdb05237" /><br/>  

For a quick short note, you can select or edit the note in the combobox. For additional comments or clarification, you can add more info in the optional comments box. The combined text will be available in the label of the pointfeature that will be created.  

>[!NOTE]
>The combined length of the note is limited to a minimum of 3 characters, and a maximum of 190 characters. The OK button will not be available outside these limits. The total number of characters is shown at the bottom-right, below the commentsbox.  

As soon as you click OK, the plugin will add a memory-layer to the map legend with a default styling and the first marker added. The marker will show up on the map as a bright yellow pointfeature with a red label attached. If you'd like to modify the comment, or remove the marker, use the corresponding buttons.  

>[!NOTE]
>To ease the process of placing multiple markers, the marker MapTool also allows panning the map. Hold the mousebutton while moving the pointer to pan the map.  

**Contextmenu**  
To make it even more convenient to place a marker, you can also right-click the map at a desired location using the right-mouse button. This will show the MapCanvas contextmenu which will have an additional submenu called "Markers". It represents the same actions as the buttons, except adding a marker is immediate since the maplocation is already known by the menu-mouse-click.

<img width="412" height="123" alt="image" src="https://github.com/user-attachments/assets/91d21e4e-9900-4d17-becc-2472c7f05756" /><br/>  

#
### Session mode  
Session mode allows you to organize your work in batches. It stores markers in a folder-structure, logs the actions, supports quick access and also enables some customization. The Session-mode function basically creates, in advance, a markerlayer with a folder-reference. The folder contains storage for markers, a log file, a styling file, and a notes list. This allows you to harvest statistics and customize behavior. It also enables the plugin to offer additional convenience. It will save markers as separate GeoJSON items, and will reload those items if the corresponding session-layer is encountered. 

Starting a Session is simple. Click the sessionmenu button, and choose "Start...":

<img width="253" height="124" alt="image" src="https://github.com/user-attachments/assets/2c367ea9-babb-4700-9e67-ffbf02d9a8c9" /><br/>  

The plugin will then ask you to enter or choose a Sessionname:

<img width="384" height="185" alt="image" src="https://github.com/user-attachments/assets/717b0ef3-77f0-421c-bd8f-44b74cfc0dc8" /><br/>

For convenience, the current date is provided in numbers. You do not have to use it. Any name can be chosen. Both the layer and the folder will use this name. (If your system has restrictions on foldernames, apply those same restrictions to the name you enter.) If you have created Sessions previously, they will be available as items in the combobox. They will also show up as items beneath the "Start..." option. If you want to reopen a previous session, you can use either option to quickly open the session desired.

>[!IMPORTANT]
>**Central Storage Location**  
>The plugin requires a central storage location in order to save the session folders. The first time you start a session, the plugin will ask you to assign a central storage location. The storage location is simply a path to a folder of your liking wherein the session folders will be created. You can change the central storage path whenever you want by choosing _Sessionmenu->Options..._
>
><img width="342" height="197" alt="image" src="https://github.com/user-attachments/assets/2cdf7aec-f0bc-4172-9cff-c2649b4ffe97" /><br/>
>
>This can also be used as another way to organize your work. You can select a new folder at the start of each month for example, or you can create multiple folders for different registries.








