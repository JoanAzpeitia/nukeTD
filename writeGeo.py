####automatization of writeGeo render node for nuke, rendering ABC or FBX####

import nuke
import os

def writeGeoABC():
    # find shot path
    scriptPath = nuke.root().name()
    relativePath = os.path.split(scriptPath)[0]
    elementsDir = os.path.split(relativePath)[0] + '/elements/nukeExports/'

    writeGeoNode = nuke.createNode('WriteGeo')
    # create name
    name = writeGeoNode['name'].value()
    namePath = name + 'NukeAlembicExport'
    # check ext
    ext = writeGeoNode['file_type'].setValue('abc')
    extPath = 'abc'
    # build Write Geo path
    geoPath = elementsDir + namePath + '.' + extPath
    writeGeoNode.knob('file').setValue(geoPath)


def writeGeoFBX():
    # find shot path
    scriptPath = nuke.root().name()
    relativePath = os.path.split(scriptPath)[0]
    elementsDir = os.path.split(relativePath)[0] + '/elements/nukeExports/'

    writeGeoNode = nuke.createNode('WriteGeo')
    # create name
    name = writeGeoNode['name'].value()
    namePath = name + 'nukeFBXExport'
    # check ext
    ext = writeGeoNode['file_type'].setValue('fbx')
    extPath = 'fbx'
    # build Write Geo path
    geoPath = elementsDir + namePath + '.' + extPath
    writeGeoNode.knob('file').setValue(geoPath)
