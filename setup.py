import maya.cmds as mc

currentTab = mc.shelfTabLayout('ShelfLayout', st = True, q = True) 
mc.shelfButton(p = currentTab, ann = 'Click to create Ground Plane, Double-Click for Options', c = 'import GroundPlane_Final \nGroundPlane_Final.executeGPTool()', dcc = 'import GroundPlane_Final \nGroundPlane_Final.optionsWindow()', label = 'GroundPlane', iol = 'GrdPln', i = 'polyPlane.png')