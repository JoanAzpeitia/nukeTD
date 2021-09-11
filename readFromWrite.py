####Read from Write for common nuke write node####
####Using clique module to fin sequence ranges####

import nuke
import os
import sys

sys.path.append("C:\\Python27\\Lib\\site-packages")
sys.path.append("C:\\Python27\\Lib\\site-packages\\clique-1.5.0-py2.7.egg")
import clique


def readFromWrite():
    node = nuke.selectedNode()
    renderPath = node.knob('file').getValue()
    colorspace = node.knob('colorspace').getValue()
    colorspace2 = int(colorspace)
    renderFolder = str(os.path.dirname(renderPath))
    items = os.listdir(renderFolder)
    if not os.path.isdir(renderFolder):
        message = 'Render folder does not exist'
        nuke.message(message)
        raise RuntimeError(message)

    collections, remainder = clique.assemble(items)

    if not collections == []:
        renderCollection = collections[0]
        start, end = min(renderCollection.indexes), max(renderCollection.indexes)

        ###create read node###
        read_node = nuke.createNode("Read")
        read_node["file"].setValue(renderPath.replace('\\', '/'))
        read_node["first"].setValue(start)
        read_node["last"].setValue(end)
        read_node["origfirst"].setValue(start)
        read_node["origlast"].setValue(end)
        read_node.knob("colorspace").setValue(colorspace2)

    else:
        message = 'Could not find your rendered path'
        nuke.message(message)
        raise RuntimeError(message)


