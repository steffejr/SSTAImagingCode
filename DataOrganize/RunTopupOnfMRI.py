import os
import sys

# _thisDir = os.path.dirname(os.path.abspath(__file__))
# import parameters from a config file
# sys.path.append(os.path.join(_thisDir))

from NCM002_Import_Config import *
# Perform topup analysis on fMRI data
import MRIDataImport

BaseDir = MRIDataImport.FindBaseDirectory(LabName, StudyName, DataPath)
PartID = '1002023'
Visitid = 'V001'

# Find the Expected Files 
# P >> A file
PAPath = os.path.join(BaseDir, 'ProcMRIData', PartID, Visitid, 'fMRI_Phase_PA', ProcessedNIIFileFolderName)
PAFileName =  "%s_%s_%s.%s"%(PartID,Visitid,'fMRI_Phase_PA', 'nii')
PAFilePath = os.path.join(PAPath, PAFileName)
# A >> P file
APPath = os.path.join(BaseDir, 'ProcMRIData', PartID, Visitid, 'fMRI_Phase_AP', ProcessedNIIFileFolderName)
APFileName =  "%s_%s_%s.%s"%(PartID,Visitid,'fMRI_Phase_AP', 'nii')
APFilePath = os.path.join(APPath, APFileName)



# Do the files exist?
if os.path.exists(PAFilePath) and os.path.exists(APFilePath):
    # print("Good to go!")
    print('\t>>> Setting up data for topup')
    # Make a log file in the AP folder
    fidlog = open(os.path.join(APPath,'RuningAndApplyingTopup.log'),'w')
    
    APOneFilePath = os.path.join(APPath, "%s_%s_%s.%s"%(PartID,Visitid,'fMRI_Phase_AP_001', 'nii'))
    PAOneFilePath = os.path.join(PAPath, "%s_%s_%s.%s"%(PartID,Visitid,'fMRI_Phase_PA_001', 'nii'))
    MergedAPPAFilePath = os.path.join(APPath, "%s_%s_%s"%(PartID,Visitid,'fMRI_Phase_Merged_AP_PA'))
    # Extract the first image from each file
    Str = "fslroi %s %s 0 1"%(APFilePath, APOneFilePath)
    print(Str)
    fidlog.write('\n\n')    
    fidlog.write(Str)
    os.system(Str)
    
    Str = "fslroi %s %s 0 1"%(PAFilePath, PAOneFilePath)
    print(Str)
    fidlog.write('\n\n')
    fidlog.write(Str)
    os.system(Str)
    # Merge these two files together
    Str = "fslmerge -t %s %s %s"%(MergedAPPAFilePath,APOneFilePath,PAOneFilePath)
    print(Str)
    fidlog.write('\n\n')
    fidlog.write(Str)    
    os.system(Str)
    # Make the acquisitions file
    AcqFilePath = os.path.join(APPath, 'datain.txt')
    fid = open(AcqFilePath, 'w')
    fid.write('0 1 0 0.043632')
    fid.write('\n')
    fid.write('0 -1 0 0.043632')
    fid.write('\n')
    fid.close()
    ApplyAcqFilePath = os.path.join(APPath, 'ApplyDatain.txt')
    fid = open(ApplyAcqFilePath, 'w')
    fid.write('0 1 0 0.010908')
    fid.write('\n')
    fid.write('0 -1 0 0.010908')
    fid.write('\n')
    fid.close()    
    # Run topup
    UnwarpedFilePath = os.path.join(APPath, "%s_%s_%s"%(PartID,Visitid,'fMRI_Phase_unwarped'))
    Str = 'topup --imain=%s --datain=%s --config=b02b0.cnf --fout=my_fieldmap --out=%s'%(MergedAPPAFilePath, AcqFilePath, UnwarpedFilePath)
    print(Str)
    fidlog.write('\n\n')
    fidlog.write(Str)    
    print('\t>>> Running top up')
    os.system(Str)

    # Apply topup to the fMRI data
    # Cycle over all fMRI files for this person
    count = 0
    for i in AllImports:
        if i['SearchString'] == 'fMRI':
            # while count < 1:
                count += 1
                print('\t>>> Working on %s'%(i['FileNameTag']))
                InDataPath = os.path.join(BaseDir, 'ProcMRIData', PartID, Visitid, i['Foldername'],ProcessedNIIFileFolderName)
                InDataName = "%s_%s_%s"%(PartID,Visitid,i['FileNameTag'])
                # Does the file exist?
                InData = os.path.join(InDataPath, InDataName)
                # Append 'u' to the beginning of the data name
                Prefix = 'u'
                UnwarpedOutFolderName = 'uspm12'
                OutDataPath = os.path.join(os.path.split(InDataPath)[0],UnwarpedOutFolderName)
                # If the folder does not exist, make it
                if not os.path.exists(OutDataPath):
                    os.mkdir(OutDataPath)
                    
                OutDataName = "%s%s_%s_%s"%(Prefix, PartID,Visitid,i['FileNameTag'])
                OutData = os.path.join(OutDataPath, OutDataName)
                Str = 'applytopup --imain=%s --inindex=1 --method=jac --datain=%s --topup=%s --out=%s --verbose'%(InData, ApplyAcqFilePath, UnwarpedFilePath, OutData)
                # print(Str)
                print('\t>>> Running applytopup')
                fidlog.write('\n\n')
                fidlog.write(Str)            
                os.system(Str)
                # Unzip the created file
                if os.path.exists(os.path.join(OutData+'.nii.gz')):
                    Str = 'gunzip %s'%(os.path.join(OutData+'.nii.gz'))
                    print(Str)
                    fidlog.write('\n\n')                    
                    fidlog.write(Str)            
                    os.system(Str)
fidlog.close()
                