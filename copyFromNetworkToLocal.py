####custome localization of files in Nuke software####
#### it basically copies the files from your selected Read node or it removes them from your local hardcoded path####



import nuke
import shutil
import os
#import threading
#import time

def copyFilesToLocal():

    try:
        progBar = nuke.ProgressTask("Progress job")
        read_node = nuke.selectedNode()
        source_path = read_node['file'].value()
        source_folder = os.path.dirname(source_path)
        source_folder_len = len(source_folder)
        source_folder_02 = source_folder[2:source_folder_len]
        target_folder = "D:" + source_folder_02
        file_list = os.listdir(source_folder)

        for i, filename in enumerate(file_list):
            if progBar.isCancelled():
                break;
            try:
                if os.path.isdir(target_folder) == False:
                    old_umask = os.umask(0)
                    os.makedirs(target_folder, 0777)
                    os.umask(old_umask)
                progBar.setMessage('Copying file {}'.format(filename))
                progBar.setProgress(int(float(i) / len(file_list) * 100))
                shutil.copy(os.path.join(source_folder, filename), target_folder)
                read_node['label'].setValue('@localized2')
                length = len(source_path)
                source_pathNoDisk = source_path[2:length]
                localDiskLetter = 'D:'
                proxiePath = localDiskLetter + source_pathNoDisk
                read_node.knob('proxy').setValue(proxiePath)
                nuke.root().knob('proxy_scale').setValue(1)
                nuke.root().knob('proxy').setValue(1)

            except:
                message1 = "the file you are trying to copy already exists"
                nuke.message(message1)
    except:
        message = "Please check that you selected your Read Node, couldn't copy the files"
        nuke.message(message)

def removeFilesFromLocal():

    node = nuke.selectedNode()
    proxieValue = node.knob('proxy').value()
    proxieDirectory = os.path.dirname(proxieValue)
    #print proxieDirectory
    try:

        node.knob('proxy').setValue("")
        node.knob('label').setValue("")
        shutil.rmtree(proxieDirectory)
        messageRemove = "your plate folder has been removed from D"
        nuke.message(messageRemove)
    except:
        notRemovedMessage = "there's been a problem, your files have not been removed"
        nuke.message(notRemovedMessage)
