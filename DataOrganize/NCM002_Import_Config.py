# It would be great to have this setup also take folder names. This is because 
# I do not need a separate folder for images that should stay together. 
# As an example, DTI and the two images for topup adjustment.

# What is the name of the lab. We use this as a top level folder name 
LabName = 'NCMLab'
# Within the lab folder there is study folder
StudyName = 'NCM002-MRIStudy'
# What is the 
DataPath = '/media/jsteffener/Data002/NCMLab'

# This is path the dcm2nii 
# I anticipate since this file is saved in a synced folder that there should not be
# multiple copies of this file on each computer. This may be a problem if there
# are differnet locations for mricron/dcm2nii

dcm2niiPath = '/usr/bin/dcm2nii'
# Two copies of each MRI file will be made in the processed folder. One is an
# original copy of the data that is NOT to be touched.
OriginalNIIFileFolderName = 'OriginalFile'
# The second copy of the data is in this folder and is for processing. Therefore,
# if the datagets screwed up a new copy of the data can be easily made. Or if a new
# version of the software is to be used then that is possible also.
ProcessedNIIFileFolderName = 'spm12'
# What folders need to be made for stats analyses
StatsFoldersList = ['DMS', 'VSTM','NBack']
# Extra useful folders
ExtraFolders = ['jobs']
        
AllImports = []
thisEntry = {'Name' : 'DTI',
        'SearchString' : 'diff64dir',
        'FileNameTag' : 'DTI',                
        'Foldername' : 'DTI',          
        'Extension' : 'nii'}       
AllImports.append(thisEntry)

thisEntry = {'Name' : 'DTI bvec',
        'SearchString' : 'diff64dir',
        'FileNameTag' : 'DTI',     
        'Foldername' : 'DTI',     
        'Extension' : 'bvec'}       
AllImports.append(thisEntry)

thisEntry = {'Name' : 'DTI bval',
        'SearchString' : 'diff64dir',
        'FileNameTag' : 'DTI',        
        'Foldername' : 'DTI',               
        'Extension' : 'bval'}       
AllImports.append(thisEntry)

thisEntry = {'Name' : 'DTI Diff P>>A',
        'SearchString' : 'diffPA',
        'FileNameTag' : 'DTI_DiffPA',
        'Foldername' : 'DTI',        
        'Extension' : 'nii'}               
AllImports.append(thisEntry)           

thisEntry = {'Name' : 'T1',
        'SearchString' : 'MEMPRAGE',
        'FileNameTag' : 'T1',
        'Foldername' : 'T1',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True}       
AllImports.append(thisEntry)

thisEntry = {'Name' : 'fMRI Phase Mapping A>>P',
        'SearchString' : 'fMRIRefAP',
        'FileNameTag' : 'fMRI_Phase_AP',
        'Foldername' : 'fMRI_Phase',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':False}               
AllImports.append(thisEntry)       

thisEntry = {'Name' : 'fMRI Phase Mapping P>>A',
        'SearchString' : 'fMRIRefPA',
        'FileNameTag' : 'fMRI_Phase_PA',
        'Foldername' : 'fMRI_Phase',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':False}               
AllImports.append(thisEntry)       


thisEntry = {'Name' : 'DMS First Administration',
        'SearchString' : 'fMRI',
        'FileNameTag' : 'DMSRun1',
        'Foldername': 'DMSRun1',
        'Extension' : 'nii',
        'NeedAnalysisFolder':True}       
AllImports.append(thisEntry)    

thisEntry = {'Name' : 'DMS Second Administration',
        'SearchString' : 'fMRI',
        'FileNameTag' : 'DMSRun2',
        'Foldername' : 'DMSRun2',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True}       
AllImports.append(thisEntry)    

thisEntry = {'Name' : 'VSTM First Administration',
        'SearchString' : 'fMRI',
        'FileNameTag' : 'VSTMRun1',
        'Foldername' : 'VSTMRun1',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True}       
AllImports.append(thisEntry)    

thisEntry = {'Name' : 'VSTM Second Administration',
        'SearchString' : 'fMRI',
        'FileNameTag' : 'VSTMRun2',
        'Foldername' : 'VSTMRun2',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True}       
AllImports.append(thisEntry)    

thisEntry = {'Name' : 'N-Back First Administration',
        'SearchString' : 'fMRI',
        'FileNameTag' : 'NBackRun1',
        'Foldername' : 'NBackRun1',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True}       
AllImports.append(thisEntry)    

thisEntry = {'Name' : 'N-Back Second Administration',
        'SearchString' : 'fMRI',
        'FileNameTag' : 'NBackRun2',
        'Foldername' : 'NBackRun2',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True}       
AllImports.append(thisEntry)    

thisEntry = {'Name' : 'ASL',
        'SearchString' : '3DASL',
        'FileNameTag' : 'ASL',
        'Foldername' : 'ASL',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True}       
AllImports.append(thisEntry)    

thisEntry = {'Name' : 'ASL M0',
        'SearchString' : 'M03DASL',
        'FileNameTag' : 'ASLM0',
        'Foldername' : 'ASL',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':False}       
AllImports.append(thisEntry)  

thisEntry = {'Name' : 'NeuroMel',
        'SearchString' : 'goldStarNM',
        'FileNameTag' : 'NeuroMel',
        'Foldername' : 'NeuroMel',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True}      
AllImports.append(thisEntry)      