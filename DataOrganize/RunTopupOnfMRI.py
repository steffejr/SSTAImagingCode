import os
import sys

# _thisDir = os.path.dirname(os.path.abspath(__file__))
# import parameters from a config file
# sys.path.append(os.path.join(_thisDir))

from NCM002_Import_Config import *
# Perform topup analysis on fMRI data
import MRIDataImport

BaseDir = MRIDataImport.FindBaseDirectory(LabName, StudyName, DataPath)
PartID = '2002036'
Visitid = 'V001'

# Expected Files 
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
    print("Good to go!")
    

APOneFilePath = os.path.join(APPath, "%s_%s_%s.%s"%(PartID,Visitid,'fMRI_Phase_PA_001', 'nii'))
PAOneFilePath = os.path.join(PAPath, "%s_%s_%s.%s"%(PartID,Visitid,'fMRI_Phase_AP_001', 'nii'))
MergedAPPAFilePath = os.path.join(APPath, "%s_%s_%s.%s"%(PartID,Visitid,'fMRI_Phase_Merged_AP_PA', 'nii'))
# Extract the first image from each file
os.system("fslroi %s %s 0 1"%(APFilePath, APOneFilePath))
os.system("fslroi %s %s 0 1"%(PAFilePath, PAOneFilePath))
# Merge these two files together
os.system("fslmerge -t %s %s %s"%(MergedAPPAFilePath,APOneFilePath,PAOneFilePath))
# Make the acquisitions file
AcqFilePath = os.path.join(APPath, 'datain.txt')
fid = open(AcqFilePath, 'w')
fid.write('0 1 0 0.0448')
fid.write('\n')
fid.write('0 -1 0 0.0448')
fid.write('\n')
fid.close()
# Run topup
UnwarpedFilePath = os.path.join(APPath, "%s_%s_%s.%s"%(PartID,Visitid,'fMRI_Phase_unwarped', 'nii'))
os.system('topup --imain=%s --datain=%s --config=b02b0.cnf --fout=my_fieldmap --iout=%s'%(MergedAPPAFilePath, AcqFilePath, UnwarpedFilePath))
