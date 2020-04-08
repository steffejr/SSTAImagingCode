# -*- coding: utf-8 -*-
"""
Reorder the NII files
@author: jason
"""
import glob
import os
#import nibabel as nib
import shutil
import sys
# Find the folders for this computer.
# Since the location of the team drive may differ on each computer this script
# is written to figure out where it is before it does anything.

# Make a feature so that if a scan name is entered as an extra parameter then 
# the program will only run and copy over that one scan. This is good to correct 
# 9spopopmistakes.

LabName = 'NCMLab'
StudyName = 'NCM002-MRIStudy'

# Start with this script's folder
ThisScript = os.path.dirname(os.path.realpath(__file__))
# Now find the Base folder
# First, split the path
splitThisScript = ThisScript.split(os.path.sep)
# Find where the lab name is
ind = splitThisScript.index(LabName)
BaseDir = os.path.join(*splitThisScript[0:ind+1])
BaseDir = os.path.join(os.path.sep, BaseDir, StudyName, 'Data', 'Imaging')



def FindFile(Tag, LookingFor,NIIFiles):
    # All of the scans off of the PERFORM scanner have the same "LookingFor" label.
    # The tag is what I want to call it.
    match = [s for s in NIIFiles if LookingFor in s]
    if isinstance(match,list):
        if len(match) > 1:
            for i in range(0,len(match)):
                print (" %s \t %d \t %d"%(match[i], i+1,os.path.getsize(match[i])))
                # print ("%d \t %d \t %s"%(i+1,os.path.getsize(match[i]),match[i]))
            sel = input(("Select file for: %s . Press [return] to skip  ")%(Tag))
            if len(sel) > 0:
                match = match[int(sel)-1]
            else:
                return
        else:
            match = match[0]
        print("Using: %s"%(match))
    return match
        
def MoveFile(FilePath, VisProcMRIFolder, Subid, Visitid, Type, Ext = 'nii'):
    # make the folder
    # make new name

    AnalysisFolderName = 'spm12'
    OutName = "%s_%s_%s.%s"%(Subid,Visitid,Type, Ext)
    os.mkdir(os.path.join(VisProcMRIFolder,Type))
    os.mkdir(os.path.join(VisProcMRIFolder,Type,AnalysisFolderName))
    shutil.copy(FilePath,os.path.join(VisProcMRIFolder,Type,OutName))
    shutil.copy(FilePath,os.path.join(VisProcMRIFolder,Type,AnalysisFolderName,OutName))
    
    
if len(sys.argv) < 2:
    print('Usage: OrganizeNII.py <SubjectID> <VisitID>')
    sys.exit(0)
else:
    StudyName = "NCM"
    Subid = "%3d"%(int(sys.argv[1]))
    Visitid = "V%03d"%(int(sys.argv[2]))
    print(Subid)
    print(Visitid)
    RawMRIFolder = os.path.join(BaseDir,"RawMRIData",Subid)
    # BehavDataFolder = os.path.join(BaseDir,"BehavioralData",Subid)        
    ProcMRIFolder = os.path.join(BaseDir,"ProcMRIData",Subid)

    VisRawMRIFolder = os.path.join(BaseDir,"RawMRIData",Subid,Visitid)
    # VisBehavDataFolder = os.path.join(BaseDir,"BehavioralData",Subid,Visitid)        
    VisProcMRIFolder = os.path.join(BaseDir,"ProcMRIData",Subid,Visitid)
    print(VisRawMRIFolder)
    # Check to make sure the BaseDir exists
    # If so then check to make sure NONE of the Subject folders exists
#    print(not os.path.exists(VisRawMRIFolder)) 
#    print(not os.path.exists(VisBehavDataFolder)) 
#    print(not os.path.exists(VisProcMRIFolder))
    if (( os.path.exists(VisRawMRIFolder)) & ( os.path.exists(VisProcMRIFolder))):
#    if (~os.path.exists(VisRawMRIFolder)) & (~os.path.exists(VisBehavDataFolder)) & (~os.path.exists(VisProcMRIFolder)):
        print
        print("Subject: %s is not in the system yet!"%(Subid))
        print
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # Make folders that are useful for processing
        os.mkdir(os.path.join(VisProcMRIFolder,"jobs"))
        os.mkdir(os.path.join(VisProcMRIFolder,"fmriResults"))
        os.mkdir(os.path.join(VisProcMRIFolder,"fmriResults","VSTM"))
        os.mkdir(os.path.join(VisProcMRIFolder,"fmriResults","VSTM","model1"))
        os.mkdir(os.path.join(VisProcMRIFolder,"fmriResults","DMS"))
        os.mkdir(os.path.join(VisProcMRIFolder,"fmriResults","DMS","model1"))        
        os.mkdir(os.path.join(VisProcMRIFolder,"fmriResults","NBack"))                
        os.mkdir(os.path.join(VisProcMRIFolder,"fmriResults","NBack","model1"))                        
########################################        


        print
        print("Select the DTI image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("DTI","diff64dir",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "DTI")      
        # Make sure to also move the bvec and bval files also
        print
        print("Select the DTI BVEC file")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.bvec'))
        # print(NIIFiles)
        T1 = FindFile("DTI","diff64dir",NIIFiles)
        Ext = 'bvec'
        Type = 'DTI'
        AnalysisFolderName = 'spm12'
        OutName = "%s_%s_%s.%s"%(Subid,Visitid,Type, Ext)
        shutil.copy(T1,os.path.join(VisProcMRIFolder,Type,OutName))
        shutil.copy(T1,os.path.join(VisProcMRIFolder,Type,AnalysisFolderName,OutName))
        print
        print("Select the DTI BVAL file")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.bval'))
        # print(NIIFiles)
        T1 = FindFile("DTI","diff64dir",NIIFiles)
        Ext = 'bval'
        Type = 'DTI'        
        AnalysisFolderName = 'spm12'
        OutName = "%s_%s_%s.%s"%(Subid,Visitid,Type, Ext)
        shutil.copy(T1,os.path.join(VisProcMRIFolder,Type,OutName))
        shutil.copy(T1,os.path.join(VisProcMRIFolder,Type,AnalysisFolderName,OutName))

########################################
        # find T1 
        print
        print("Select the T1 image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("anat","MEMPRAGE",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "T1")        
########################################
        print
        print("Select the DMS Run One image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("DMSRun1","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "DMSRun1")     

        print
        print("Select the DMS Run Two image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("DMSRun2","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "DMSRun2")     
########################################        
        print
        print("Select the VSTM Run One image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("VSTMRun1","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "VSTMRun1")     

        print
        print("Select the VSTM Run Two image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("VSTMRun2","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "VSTMRun2")     
########################################        
        print
        print("Select the N-Back Run One image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("NBackRun1","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "NBackRun1")     

        print
        print("Select the N-Back Run Two image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("NBackRun2","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "NBackRun2")     
        
########################################        
        print
        print("Select the ASL image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("ASL","3DASL",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "ASL")     

        print
        print("Select the ASL M0 image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("ASLM0","M03DASL",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "ASLM0")     
########################################
        print
        print("Select the Neuromelanin image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # print(NIIFiles)
        T1 = FindFile("NeuroMel","goldStarNM",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "NeuroMel")     
    else:
        print('Cannot find data')                    
        print('Looking for raw MRI data here: \n\t%s'%(VisRawMRIFolder))
        print('Looking for processed MRI folder here: \n\t%s'%(VisProcMRIFolder))        
