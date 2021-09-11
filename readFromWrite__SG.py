#### Read from Write for Shotgun WriteTank gizmo####
#### it uses clique library to find sequnce ranges####



import nuke
import os
import clique

def readFromWrite():
    node = nuke.selectedNode()
    sequence = os.path.join(
        node.knobs()['path_context'].value(),
        node.knobs()['path_local'].value(),
        node.knobs()['path_filename'].value()
    )
    folder = os.path.dirname(sequence)
    items = os.listdir(folder)
    if not os.path.isdir(folder):
        message = 'Render folder does not exist'
        nuke.message(message)
        raise RuntimeError(message)

    collections, remainder = clique.assemble(items)

    if collections == []:
        renderPath = remainder[0]
        splitRenderPath = os.path.splitext(renderPath)
        renderPath01 = splitRenderPath[0]
        lengthRenderName = len(renderPath01)
        lengthRenderNameNoPad = lengthRenderName - 4
        framePadding = renderPath01[lengthRenderNameNoPad: lengthRenderName]
        intFramePadding = int(framePadding)

        ###create read node###
        read_node = nuke.createNode("Read")
        read_node["file"].setValue(sequence.replace('\\', '/'))
        read_node["first"].setValue(intFramePadding)
        read_node["last"].setValue(intFramePadding)
        read_node["origfirst"].setValue(intFramePadding)
        read_node["origlast"].setValue(intFramePadding)

    elif not collections == []:
        renderCollection = collections[0]
        start, end = min(renderCollection.indexes), max(renderCollection.indexes)

        ###create read node###
        read_node = nuke.createNode("Read")
        read_node["file"].setValue(sequence.replace('\\', '/'))
        read_node["first"].setValue(start)
        read_node["last"].setValue(end)
        read_node["origfirst"].setValue(start)
        read_node["origlast"].setValue(end)

    else:
        message = 'Could not find your rendered path'
        nuke.message(message)
        raise RuntimeError(message)
