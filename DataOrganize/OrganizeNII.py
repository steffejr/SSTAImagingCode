
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 10:08:31 2015

Reorder the NII files
@author: jason
"""
import glob
import os
#import nibabel as nib
import shutil
import sys

def FindFile(Tag, LookingFor,NIIFiles):
    # All of the scans off of the PERFORM scanner have the same "LookingFor" label.
    # The tag is what I want to call it.
    match = [s for s in NIIFiles if LookingFor in s]
    if isinstance(match,list):
        if len(match) > 1:
            for i in range(0,len(match)):
                print ("%d \t %d \t %s"%(i+1,os.path.getsize(match[i]),match[i]))
            sel = input(("Select file for: %s . Press [return] to skip")%(Tag))
            if len(sel) > 0:
                match = match[int(sel)-1]
            else:
                return
        else:
            match = match[0]
        print("Using: %s"%(match))
    return match
        
def MoveFile(FilePath, VisProcMRIFolder, Subid, Visitid, Type):
    # make the folder
    # make new name
    AnalysisFolderName = 'spm12'
    OutName = "%s_%s_%s.nii"%(Subid,Visitid,Type)
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
#    BaseDir = os.path.join("/Users","jason","Documents","MyData","Olfaction","OlfTrain")
#    BaseDir = os.path.join("/media","jsteffen","Data001","NeuralCognitiveMapping","Imaging")
    BaseDir = os.path.join("/media","jsteffen","JASONDATA","NCM001","Imaging")
    RawMRIFolder = os.path.join(BaseDir,"RawMRIData",Subid)
    BehavDataFolder = os.path.join(BaseDir,"BehavioralData",Subid)        
    ProcMRIFolder = os.path.join(BaseDir,"ProcMRIData",Subid)

    VisRawMRIFolder = os.path.join(BaseDir,"RawMRIData",Subid,Visitid)
    VisBehavDataFolder = os.path.join(BaseDir,"BehavioralData",Subid,Visitid)        
    VisProcMRIFolder = os.path.join(BaseDir,"ProcMRIData",Subid,Visitid)
    print(VisRawMRIFolder)
    # Check to make sure the BaseDir exists
    # If so then check to make sure NONE of the Subject folders exists
#    print(not os.path.exists(VisRawMRIFolder)) 
#    print(not os.path.exists(VisBehavDataFolder)) 
#    print(not os.path.exists(VisProcMRIFolder))
    if ((not os.path.exists(VisRawMRIFolder)) & (not os.path.exists(VisBehavDataFolder)) & (not os.path.exists(VisProcMRIFolder))):
#    if (~os.path.exists(VisRawMRIFolder)) & (~os.path.exists(VisBehavDataFolder)) & (~os.path.exists(VisProcMRIFolder)):
        print
        print("Subject: %s is not in the system yet!"%(Subid))
        print
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        # Make folders that are useful for processing
        os.mkdir(os.path.join(VisProcMRIFolder,"jobs"))
        os.mkdir(os.path.join(VisProcMRIFolder,"fmriResults"))
        os.mkdir(os.path.join(VisProcMRIFolder,"fmriResults","Model1"))
########################################        
        # find T1 
        print
        print("Select the T1 image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        print(NIIFiles)
        T1 = FindFile("anat","MEMPRAGE",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "T1")        
########################################
        print
        print("Select the DMS Run One image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        print(NIIFiles)
        T1 = FindFile("DMSRun1","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "DMSRun1")     

        print
        print("Select the DMS Run Two image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        print(NIIFiles)
        T1 = FindFile("DMSRun2","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "DMSRun2")     
########################################        
        print
        print("Select the VSTM Run One image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        print(NIIFiles)
        T1 = FindFile("VSTMRun1","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "VSTMRun1")     

        print
        print("Select the VSTM Run Two image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        print(NIIFiles)
        T1 = FindFile("VSTMRun2","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "VSTMRun2")     
########################################        
        print
        print("Select the Semantic Rich Run One image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        print(NIIFiles)
        T1 = FindFile("SemRichRun1","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "SemRichRun1")     

        print
        print("Select the Semantic Rich Run Two image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        print(NIIFiles)
        T1 = FindFile("SemRichRun2","fMRI",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "SemRichRun2")     
        
########################################        
        print
        print("Select the ASL image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        print(NIIFiles)
        T1 = FindFile("ASL","3DASL",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "ASL")     

        print
        print("Select the ASL M0 image")
        NIIFiles = glob.glob(os.path.join(VisRawMRIFolder,'*.nii'))
        print(NIIFiles)
        T1 = FindFile("ASLM0","M03DASL",NIIFiles)
        MoveFile(T1, VisProcMRIFolder, Subid, Visitid, "ASLM0")     
        