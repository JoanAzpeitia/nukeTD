####before Nuke 12 we did not have the option to create directories in the Write Node####
####the callback to do so, beforeRender() didn't work for SG WriteTank, thus I developed this snippet to do so in all WriteTank nodes in our Nuke scene####

import nuke
import os

def createDirectories():
    for node in nuke.allNodes():
        if node.Class() == 'WriteTank':
            sequence = os.path.join(
                node.knobs()['path_context'].value(),
                node.knobs()['path_local'].value(),
                node.knobs()['path_filename'].value()
            )
            folder = os.path.dirname(sequence)
            if os.path.exists(folder) == True:
                print 'render directory was already created'
            else:
                os.makedirs(folder)
                print 'render directory directory has been created'