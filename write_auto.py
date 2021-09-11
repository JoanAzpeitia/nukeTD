####automatization of nuke's write node settings regarding your scene settings###

import os
import nuke



def writeEXR():
    scriptPath = nuke.root()['name'].value()
    scriptEnvPath = os.path.dirname(os.path.dirname(scriptPath))
    shotEnvPath = os.path.dirname(os.path.dirname(scriptEnvPath))
    splitScriptPath = os.path.split(scriptPath)
    scriptExt = splitScriptPath[1]
    scriptExt01 = os.path.splitext(scriptExt)
    scriptName = scriptExt01[0]
    renderPath = os.path.join(shotEnvPath, "comp", "renders", scriptName, scriptName + ".%04d.exr")
    renderPath2 = renderPath.replace("\\", "/")
    crop = nuke.createNode('Crop')
    reformat = nuke.createNode('Reformat')
    reformat.knob('format').setValue("UHD_4K")
    OCIOColorSpace = nuke.createNode('OCIOColorSpace')
    OCIOColorSpace.knob('in_colorspace').setValue('ACES - ACEScg')
    OCIOColorSpace.knob('out_colorspace').setValue('ACES - ACES2065-1')
    copyMData = nuke.createNode('CopyMetaData')
    writeNode = nuke.createNode('Write')
    writeNode.knob('file').setValue(renderPath2)
    writeNode.knob('colorspace').setValue('default')
    writeNode.knob('create_directories').setValue(1)
    # writeNode.knob('write_ACES_compliant_EXR').setValue("0")
    writeNode.knob('datatype').setValue("16 bit half")
    writeNode.knob('compression').setValue(0)
    writeNode.knob('channels').setValue("rgb")
    #nuke.autoplace(crop)

    nuke.autoplace(copyMData)
    nuke.autoplace(writeNode)
    for n in nuke.allNodes() + [nuke.root(), ]:
        n.hideControlPanel()

def writePrep():
    scriptPath = nuke.root()['name'].value()
    scriptEnvPath = os.path.dirname(os.path.dirname(scriptPath))
    shotEnvPath = os.path.dirname(os.path.dirname(scriptEnvPath))
    splitScriptPath = os.path.split(scriptPath)
    scriptExt = splitScriptPath[1]
    scriptExt01 = os.path.splitext(scriptExt)
    scriptName = scriptExt01[0]
    Prep = nuke.Panel("")
    Prep.addSingleLineInput('PrepFolderName', "")
    Prep.show()
    FolderName = Prep.value('PrepFolderName')

    renderPath = os.path.join(shotEnvPath, "comp", "precomps" , FolderName , FolderName + ".%04d.exr")
    renderPath2 = renderPath.replace("\\", "/")
    writeNode = nuke.createNode('Write')
    writeNode.knob('channels').setValue("rgba")
    writeNode.knob('file').setValue(renderPath2)
    writeNode.knob('colorspace').setValue('ACES - ACEScg')
    writeNode.knob('create_directories').setValue(1)
    #writeNode.knob('write_ACES_compliant_EXR').setValue("1")
    writeNode.knob('datatype').setValue("16 bit half")
    writeNode.knob('compression').setValue(1)
    writeNode.knob('channels').setValue("rgba")
    for n in nuke.allNodes() + [nuke.root(), ]:
        n.hideControlPanel()

def writeDenoise():
    scriptPath = nuke.root()['name'].value()
    scriptEnvPath = os.path.dirname(os.path.dirname(scriptPath))
    shotEnvPath = os.path.dirname(os.path.dirname(scriptEnvPath))
    splitScriptPath = os.path.split(scriptPath)
    scriptExt = splitScriptPath[1]
    scriptExt01 = os.path.splitext(scriptExt)
    scriptName = scriptExt01[0]
    Denoise = nuke.Panel("")
    Denoise.addSingleLineInput('DenoiseFolderName', "")
    Denoise.show()
    FolderName = Denoise.value('DenoiseFolderName')

    renderPath = os.path.join(shotEnvPath, "comp", "precomps" , "Degrain" , FolderName , FolderName + ".%04d.exr")
    renderPath2 = renderPath.replace("\\", "/")
    writeNode = nuke.createNode('Write')
    writeNode.knob('channels').setValue("rgb")
    writeNode.knob('file').setValue(renderPath2)
    writeNode.knob('colorspace').setValue('ACES - ACEScg')
    writeNode.knob('create_directories').setValue(1)
    #writeNode.knob('write_ACES_compliant_EXR').setValue("1")
    writeNode.knob('datatype').setValue("16 bit half")
    writeNode.knob('compression').setValue(1)
    writeNode.knob('channels').setValue("rgba")
    for n in nuke.allNodes() + [nuke.root(), ]:
        n.hideControlPanel()
