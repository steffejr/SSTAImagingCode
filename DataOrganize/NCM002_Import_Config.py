# It would be great to have this setup also take folder names. This is because 
# I do not need a separate folder for images that should stay together. 
# As an example, DTI and the two images for topup adjustment.

# What is the name of the lab. We use this as a top level folder name 
LabName = 'JoanetteLab'
# Within the lab folder there is study folder
StudyName = 'SSTA-MRIStudy'
# What is the 
DataPath = '/Users/jasonsteffener/Documents/JoanetteLab/SSTA-MRIStudy'

# This is path the dcm2nii 
# I anticipate since this file is saved in a synced folder that there should not be
# multiple copies of this file on each computer. This may be a problem if there
# are differnet locations for mricron/dcm2nii

dcm2niiPath = '/Applications/MRIcroMTL.app/Contents/Resources/dcm2niix'
# Two copies of each MRI file will be made in the processed folder. One is an
# original copy of the data that is NOT to be touched.
OriginalNIIFileFolderName = 'OriginalFile'
# The second copy of the data is in this folder and is for processing. Therefore,
# if the datagets screwed up a new copy of the data can be easily made. Or if a new
# version of the software is to be used then that is possible also.
ProcessedNIIFileFolderName = 'spm12'
# What folders need to be made for stats analyses
StatsFoldersList = ['Semantic']
# Extra useful folders
ExtraFolders = ['jobs']
        
AllImports = []


thisEntry = {'Name' : 'T1',
        'SearchString' : 'T1w',
        'FileNameTag' : 'T1',
        'Foldername' : 'T1',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True,
        'ReconPathName':'T1w'}       
AllImports.append(thisEntry)

thisEntry = {'Name' : 'ASL',
        'SearchString' : 'asl_2d',
        'FileNameTag' : 'ASL',
        'Foldername' : 'ASL',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True,
        'ReconPathName':'asl_2d'}
AllImports.append(thisEntry)    


thisEntry = {'Name' : 'Semantic Run 1',
        'SearchString' : 'task-semantic_Run1',
        'FileNameTag' : 'SemRun1',
        'Foldername' : 'SemRun1',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True,
        'ReconPathName':'task-semantic_Run1'}      
AllImports.append(thisEntry)      

thisEntry = {'Name' : 'Semantic Run 2',
        'SearchString' : 'task-semantic_Run2',
        'FileNameTag' : 'SemRun2',
        'Foldername' : 'SemRun2',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True,
        'ReconPathName':'task-semantic_Run2'}      
AllImports.append(thisEntry)      

thisEntry = {'Name' : 'Resting State',
        'SearchString' : 'task-Resting-state_Run1',
        'FileNameTag' : 'Rest',
        'Foldername' : 'Rest',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':True,
        'ReconPathName':'task-Resting-state_Run1'}      
AllImports.append(thisEntry)      

thisEntry = {'Name' : 'fMRI Field Mapping ',
        'SearchString' : 'task-fieldmap_Run1',
        'FileNameTag' : 'FieldMapRun1',
        'Foldername' : 'SemRun1',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':False,
        'ReconPathName':'task-fieldmap_Run1'}               
AllImports.append(thisEntry)       

thisEntry = {'Name' : 'fMRI Field Mapping ',
        'SearchString' : 'task-fieldmap_Run2',
        'FileNameTag' : 'FieldMapRun2',
        'Foldername' : 'SemRun2',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':False,
        'ReconPathName':'task-fieldmap_Run2'}               
AllImports.append(thisEntry)       

thisEntry = {'Name' : 'fMRI Field Mapping ',
        'SearchString' : 'task-fieldmap_Resting',
        'FileNameTag' : 'FieldMapRest',
        'Foldername' : 'Rest',        
        'Extension' : 'nii',
        'NeedAnalysisFolder':False,
        'ReconPathName':'task-fieldmap_Resting'}               
AllImports.append(thisEntry)       
