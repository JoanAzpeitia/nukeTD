####automatization of Quicktime regarding your Read selectedNode settings####
####it uses Netflix slate gizmo as it was built for a Netflix project####


import nuke
import os

###get read exr node info###
def createQuicktime():
    try:
        ReadEXR = nuke.selectedNode()
        EXRPath = ReadEXR.knob('file').getValue()
        EXRFolder = os.path.dirname(os.path.dirname(EXRPath))
        EXRColorspace = ReadEXR.knob('colorspace').getValue()
        EXRFirst = ReadEXR.knob('first').getValue()
        EXRLast = ReadEXR.knob('last').getValue()

        ###create a group###
        group = nuke.nodes.Group()
        group.begin()

        read = nuke.createNode('Read')
        read.knob('file').setValue(EXRPath)
        read.knob('first').setValue(int(EXRFirst))
        read.knob('last').setValue(int(EXRLast))
        read.knob('colorspace').setValue(int(EXRColorspace))


        ###get shot CC File###
        scriptPath = nuke.root()['name'].value()
        shotEnvPath = os.path.dirname(os.path.dirname(scriptPath))
        shotEnvironment = os.path.dirname(os.path.dirname(shotEnvPath))
        CCPath = os.path.join(shotEnvironment, "mat_in", "CC")
        CCPath2 = CCPath.replace("\\", "/")
        CCFiles = os.listdir(CCPath2)
        CCName = []
        for f in CCFiles:
            CCName.append(f)
        file = CCPath2 + '/' + CCName[0]
        ###create OCIOCDLTRANSFORM###
        CDL = nuke.createNode('OCIOCDLTransform')
        CDL.knob('read_from_file').setValue(1)
        CDL.knob('file').setValue(file)
        CDL.knob('working_space').setValue('ACES - ACEScct')


        ###create Reformat###
        reformatHD = nuke.createNode('Reformat')
        reformatHD.knob('format').setValue("HD_1080")
        reformatHD["black_outside"].setValue(True)

        ###create Crop###
        Crop = nuke.nodePaste('Z:/Joan/.nuke/plugins/CropIDLQuicktime.nk')

        ###create Add Time Code####
        ATC = nuke.createNode('AddTimeCode')
        ATC.knob('useFrame').setValue(True)
        ATC.knob('frame').setValue(1001)

        ###create NetflixOverlay###
        NETOVER = nuke.nodePaste('Z:/Joan/.nuke/netflix_overlay_Idolo.nk')

        ###create frame counter###
        FrameCounter = nuke.createNode('Text')
        FrameCounter.knob('message').setValue('[value first_frame]-[frame]-[value last_frame]')
        FrameCounter.knob('size').setValue(20)
        FrameCounter.knob('color').setValue(0.3)
        FrameCounter.knob('box').setValue((0, 14, 1910, 1080))
        FrameCounter.knob('xjustify').setValue(2)
        FrameCounter.knob('yjustify').setValue(3)

        ###create Netflix Slate###
        NETSLT = nuke.nodePaste('Z:/Joan/NETFLIX_MEI_SLATE_IDL.nk')
        scriptPath = nuke.root()['name'].value()
        scriptEnvPath = os.path.dirname(os.path.dirname(scriptPath))
        splitScriptPath = os.path.split(scriptPath)
        scriptExt = splitScriptPath[1]
        scriptExt01 = os.path.splitext(scriptExt)
        scriptName = scriptExt01[0]
        items = scriptName.split('_')
        shotName = items[1]
        version = items[2]
        NETSLT.knob('f_version_name').setValue(scriptName)
        SubmitFor = nuke.Panel("")
        SubmitFor.addSingleLineInput('WIP or Final', "")
        SubmitFor.show()
        SubmitFor1 = SubmitFor.value('WIP or Final')
        NETSLT.knob('f_submitting_for').setValue(SubmitFor1)

        ###find shot name###
        scriptPath = nuke.root()['name'].value()
        scriptEnvPath = os.path.dirname(os.path.dirname(scriptPath))
        splitScriptPath = os.path.split(scriptPath)
        scriptExt = splitScriptPath[1]
        scriptExt01 = os.path.splitext(scriptExt)
        scriptName = scriptExt01[0]
        length = len(scriptName)
        length2 = length - 5
        ShotName = scriptName[0:length2]


        NETSLT.knob('f_shot_name').setValue(ShotName)
        ScopeWork = nuke.Panel("")
        ScopeWork.addSingleLineInput('VFX Scope of work', "")
        ScopeWork.show()
        ScopeWorkResult = ScopeWork.value('VFX Scope of work')
        NETSLT.knob('f_vfx_scope_of_work').setValue(ScopeWorkResult)

        ###create WriteNode###
        writeQT = nuke.createNode('Write')
        scriptPath = nuke.root()['name'].value()
        scriptEnvPath = os.path.dirname(os.path.dirname(scriptPath))
        shotEnvPath = os.path.dirname(os.path.dirname(scriptEnvPath))
        renderPath = shotEnvPath + '/' + 'comp'+ '/' + 'renders'
        #vfxAppend = '_vfx'
        QTFilename = renderPath + '/' + scriptName + '.mov'
        writeQT.knob('name').setValue('WriteQuicktime')
        writeQT.knob('file').setValue(QTFilename)
        writeQT.knob('colorspace').setValue("Output - Rec.709")
        writeQT.knob('mov64_codec').setValue("AVdn")
        writeQT.knob('mov64_dnxhd_codec_profile').setValue("DNxHD 422 8-bit 36Mbit")
        writeQT.knob('create_directories').setValue(True)
        ###render Quicktime###
        firstFloat = nuke.Root().knob('first_frame').getValue()
        first = int(firstFloat)
        lastFloat = nuke.Root().knob('last_frame').getValue()
        last = int(lastFloat)
        nuke.execute('WriteQuicktime', first - 1, last, 1)
        # Cleanup after ourselves
        nuke.delete(group)

        ###close all properties###
        #for n in nuke.allNodes() + [nuke.root(), ]:
        #    n.hideControlPanel()
    except:
        message = 'Select your read EXR node'
        nuke.message(message)
        raise RuntimeError(message)

