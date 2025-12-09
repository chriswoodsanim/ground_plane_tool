The Ultimate Ground Plane Tool

To install, place the "GroundPlane_Final.py" and "GroundPlane_userSettings.txt" files into this folder - 

C:\Users\<your user name>\Documents\maya\20XX\scripts

Then open yourself up a fresh Maya scene and open the script editor.

Copy the following code into a Python tab (Command > New Tab...)


\#\#\#\#\# CODE START \#\#\#\#\#

import maya.cmds as mc

currentTab = mc.shelfTabLayout('ShelfLayout', st = True, q = True)
mc.shelfButton(p = currentTab, ann = 'Click to create Ground Plane, Double-Click for Options', c = 'import GroundPlane_Final \nGroundPlane_Final.executeGPTool()', dcc = 'import GroundPlane_Final \nGroundPlane_Final.optionsWindow()', label = 'GroundPlane', iol = 'GrdPln', i = 'polyPlane.png')

##### CODE END #####


Ensuring you are on the shelf where you want this tool icon to exist, hit the "Execute All" button at the top of the script editor (the icon with 2 triangles)

This should create a shelf button.

single click will create a plane
double click will give you the options window. 

Your ground plane settings will be saved for future Maya scenes. 
