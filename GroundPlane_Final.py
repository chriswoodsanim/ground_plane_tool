import maya.cmds as mc
import os

# List of Functions


def createPlane():
    
    planeWidth = int(userSettings[1])
    planeLength = int(userSettings[2])
    
       
    # Creates plane

    mc.polyPlane(w = (planeWidth * 100), h = (planeLength * 100), sh = 8, sw = 8, n='GroundPlane_01')
    mc.group('GroundPlane_01', n='GroundPlane_GRP')

    # Creates layer and sets to reference
    if mc.objExists('SceneGEO'):
        mc.editDisplayLayerGlobals(cdl = 'SceneGEO')
        mc.editDisplayLayerMembers('SceneGEO', 'GroundPlane_GRP', nr = True)
    else:
        mc.createDisplayLayer(name='SceneGEO', nr=True)
        mc.setAttr( 'SceneGEO.displayType', 2 )
    
   
def addTexture():   

    # Creates new Lambert material
    mc.shadingNode('lambert', asShader=True, n='GroundPlane_MAT')
    mc.sets(r=True, nss=True, nw=True, n='GroundPlane_SG')
    mc.connectAttr('GroundPlane_MAT.outColor', 'GroundPlane_SG.surfaceShader')
    
    # Selects Plane and applies Checker
    mc.select('GroundPlane_01', r = True)
    mc.sets(nw=True, forceElement='GroundPlane_SG')
    
    # Sets Texture display on for the Perspective View
    mc.modelEditor(modelPanel='modelPanel4')
    mc.modelEditor( 'modelPanel4', edit=True,  dtx=True, gr=False, displayAppearance='smoothShaded',)
    
    
def addEdgeFade():
    
    # query plane shape choice
    if userSettings[0] == 'Circle' :
        planeShape = 4
        fadePosOne = 0.5
        fadePosTwo = 0.65
    else:
        planeShape = 5
        fadePosOne = 0.7
        fadePosTwo = 0.95
    
    # Creates Ramp and connects to Lambert
    mc.shadingNode('ramp', asTexture=True, n = 'groundPlaneRamp')
    mc.setAttr('groundPlaneRamp.type', planeShape)
    mc.setAttr('groundPlaneRamp.colorEntryList[0].position', fadePosOne)
    mc.setAttr('groundPlaneRamp.colorEntryList[1].position', fadePosTwo)
    mc.setAttr('groundPlaneRamp.colorEntryList[0].color',0,0,0, type='double3')
    mc.setAttr('groundPlaneRamp.colorEntryList[1].color',1,1,1, type='double3')
    
    # query edge fade check box
    if eval(userSettings[5]) == True :
        mc.setAttr('groundPlaneRamp.interpolation', 1)
    else:
        mc.setAttr('groundPlaneRamp.interpolation', 0)

        
    mc.shadingNode('place2dTexture', n = 'place2dTexture_FADE', asUtility = True)
    mc.connectAttr('place2dTexture_FADE.outUV', 'groundPlaneRamp.uv')
    mc.connectAttr('place2dTexture_FADE.outUvFilterSize', 'groundPlaneRamp.uvFilterSize')
    mc.connectAttr('groundPlaneRamp.outColor', 'GroundPlane_MAT.transparency', f = True)

def addCheckerboard():
    
    # Creates Checker and connects to Lambert
    mc.shadingNode('checker', asTexture=True, n = 'groundPlaneChecker')
    mc.setAttr('groundPlaneChecker.contrast', 0.08)
    
    checkerWidth = int(userSettings[1])
    checkerLength = int(userSettings[2])
    
    
    mc.shadingNode('place2dTexture', n = 'place2dTexture_CHCK', asUtility=True)
    mc.setAttr('place2dTexture_CHCK.repeatU', checkerWidth) 
    mc.setAttr('place2dTexture_CHCK.repeatV', checkerLength)
    mc.connectAttr('place2dTexture_CHCK.outUV', 'groundPlaneChecker.uv')
    mc.connectAttr('place2dTexture_CHCK.outUvFilterSize', 'groundPlaneChecker.uvFilterSize')
    mc.connectAttr('groundPlaneChecker.outColor', 'GroundPlane_MAT.color', f=True)
        

    
def addCentreMarkings(): 
    
    # Creates origin curves
    mc.curve(d=3, p=[(2, 0, 6),(2, 0, 3),(3, 0, 2),(6, 0, 2)], k=[0, 0, 0, 1, 1, 1])
    mc.curve(d=3, p=[(6, 0, -2),(3, 0, -2),(2, 0, -3),(2, 0, -6)], k=[0, 0, 0, 1, 1, 1])
    mc.curve(d=3, p=[(-2, 0, 6),(-2, 0, 3),(-3, 0, 2),(-6, 0, 2)], k=[0, 0, 0, 1, 1, 1])
    mc.curve(d=3, p=[(-6, 0, -2),(-3, 0, -2),(-2, 0, -3),(-2, 0, -6)], k=[0, 0, 0, 1, 1, 1])
    
    # Groups curves and Plane
    mc.group('curve1', 'curve2', 'curve3', 'curve4', n='OriginCurves_GRP')
    mc.parent('OriginCurves_GRP', 'GroundPlane_GRP')

    mc.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
    
    
def getSettings():
    
    if mc.radioButton('circleButton', q = True, sl = True):
        userSettings[0] = 'Circle'
    else:
         userSettings[0] = 'Square' 
        
    # Get lenth and width values     
    width = mc.intSliderGrp('width', q = True, v = True)
    length = mc.intSliderGrp('length', q = True, v = True)

    userSettings[1] = str(width)
    userSettings[2] = str(length)
    
    
    # Query checkerboard texture
    if mc.checkBox('CheckerButton', q =True, v = True):
        userSettings[3] = 'True'
    else:
        userSettings[3] = 'False'
    
    if mc.checkBox('OriginMarker', q = True, v = True):
        userSettings[4] = 'True'
    else:
        userSettings[4] = 'False'
        
    # checkEdgeFade
    if mc.checkBox('EdgeFade', q = True, v = True):
        userSettings[5] = 'True'
    else:
        userSettings[5] = 'False'

    
    # query anti aliasing
    if mc.checkBox('AntiAliasing', q = True, v = True):
        mc.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
        userSettings[6] = 'True'
    else:
        mc.setAttr('hardwareRenderingGlobals.multiSampleEnable', 0)
        userSettings[6] = 'False'
        
    
    filePath = str(os.path.join(os.path.dirname(__file__)))
        
    with open(filePath + '/GroundPlane_userSettings.txt', 'w') as f:
        for listItem in userSettings:
            f.write(listItem)
            f.write('\n')
        
    print(userSettings)
    
    
    
    # Deselect
    mc.select( cl=True )
    
def executeGPTool():
    
    # Check for existing plane and delete
    if mc.objExists('GroundPlane_GRP'):
        mc.select('GroundPlane_GRP')
        mc.delete()
    if mc.objExists('GroundPlane_MAT'):
        mc.select('GroundPlane_MAT')
        mc.delete()
        mc.select('GroundPlane_SG', r = True, ne = True)
        mc.delete()
    if mc.objExists('place2dTexture_CHCK'):
        mc.select('place2dTexture_CHCK')
        mc.delete()
        mc.select('groundPlaneChecker')
        mc.delete()
    if mc.objExists('place2dTexture_FADE'):
        mc.select('place2dTexture_FADE')
        mc.delete()
        mc.select('groundPlaneRamp')
        mc.delete()
        

    createPlane()
    addTexture()
    addEdgeFade()
    
    # Query checkerboard texture
    if eval(userSettings[3]) == True :
        addCheckerboard()

    # Query origin markers
    if eval(userSettings[4]) == True :
        addCentreMarkings()

    
    # query anti aliasing
    if eval(userSettings[6]) == True:
        mc.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
    else:
        mc.setAttr('hardwareRenderingGlobals.multiSampleEnable', 0)
   
    # print userSettings
    
    # Deselect
    mc.select( cl=True )

def optionsWindow():
    
    GPwindow = mc.window(title = 'The Ultimate Ground Plane Tool')
    mc.columnLayout()
    mc.text(label = 'Shape')
    mc.radioCollection()
    if userSettings[0] == 'Circle':
        mc.radioButton('circleButton', label = 'Circle', sl = True)
        mc.radioButton('squareButton', label = 'Square')
    elif userSettings[0] == 'Square':
        mc.radioButton('circleButton', label = 'Circle')
        mc.radioButton('squareButton', label = 'Square', sl = True)
    else:
        print("User settings error. line 1 in UserSettings.txt should be 'Circle' or 'Square'")
    mc.text(label = 'Size')
    mc.intSliderGrp('width', label = 'Width (m)', cal = [1, 'left'], v = int(userSettings[1]), max = 100, min = 2, field = True)
    mc.intSliderGrp('length', label = 'Length (m)', cal = [1, 'left'], v = int(userSettings[2]), max = 100, min = 2,  field = True)
    mc.text(label = 'Options')
    mc.checkBox('CheckerButton', label = 'Checkerboard Texture', v = eval(userSettings[3]))
    mc.checkBox('OriginMarker', label = 'Origin Marker', v = eval(userSettings[4]))
    mc.checkBox('EdgeFade', label = 'Edge Fade', v = eval(userSettings[5]))
    mc.checkBox('AntiAliasing', label = 'Anti Aliasing', v = eval(userSettings[6]))
    mc.button(label = 'Save and Create!', c = 'GroundPlane_Final.saveAndCreate()')
    mc.showWindow(GPwindow)



def saveAndCreate():
    
    getSettings()
    executeGPTool()
    

# Check for Window

# if mc.window('GPwindow', exists = True):
#     mc.deleteUI(GPwindow, window = True)
# else:

# GPwindow = mc.window('The Ultimate Ground Plane Tool', rtf = True)
    
    
# Get file path and define user settings list 
 
filePath = str(os.path.join(os.path.dirname(__file__)))

with open(filePath + '/GroundPlane_userSettings.txt', 'r') as f:
    userSettings = [listItem.rstrip() for listItem in f.readlines()]


