import glob

i = AllImports[6]
PartID = '2002045'
Visitid = 'V001'

VisProcMRIFolder = os.path.join(BaseDir,"ProcMRIData",PartID,Visitid)
RawMRIFolder = os.path.join(BaseDir,"RawMRIData",PartID,Visitid)

OutFileName =  "%s_%s_%s.%s"%(PartID,Visitid,i['FileNameTag'], i['Extension'])
# Create the output path for the file
OutFilePath = os.path.join(VisProcMRIFolder, i['FileNameTag'],OriginalNIIFileFolderName)


ExpectedFilePath = os.path.join(OutFilePath, OutFileName)    
# Does this file exist?
if os.path.exists(ExpectedFilePath):
    print(True)
else:
    # Add functionality for what to do if it is missing!
    # FoundFiles = glob.glob(os.path.join(RawMRIFolder, '*'+i['SearchString']+'*'+i['Extension']))


    
