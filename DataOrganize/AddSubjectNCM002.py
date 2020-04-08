import os
import sys
import glob
import shutil
import datetime
from tkinter.filedialog import askopenfilename
# Find the folders for this computer.
# Since the location of the team drive may differ on each computer this script
# is written to figure out where it is before it does anything.

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

#print("Working in the raw MRI data folder: %s" %(BaseDir))

if len(sys.argv) < 2:
    print('Usage: AddSubject.py <SubjectID (eg #)> <VisitID (eg 1)>')
    sys.exit(0)
else:
    StudyName = "NCM"
    
    Subid = "%d"%(int(sys.argv[1]))
    Visitid = "V%03d"%(int(sys.argv[2]))
  
    PathToZipInput = askopenfilename(title='Select *.tar.gz file', initialdir = '~/Downloads', filetypes = [('Zipped files','*.tar.gz')])
#    PathToZipInput = sys.argv[3]
      
    RawMRIFolder = os.path.join(BaseDir,"RawMRIData",Subid)
#    BehavDataFolder = os.path.join(BaseDir,"BehavioralData",Subid)        
    ProcMRIFolder = os.path.join(BaseDir,"ProcMRIData",Subid)

    VisRawMRIFolder = os.path.join(BaseDir,"RawMRIData",Subid,Visitid)
#    VisBehavDataFolder = os.path.join(BaseDir,"BehavioralData",Subid,Visitid)        
    VisProcMRIFolder = os.path.join(BaseDir,"ProcMRIData",Subid,Visitid)

    # Check to make sure the BaseDir exists
    # If so then check to make sure NONE of the Subject folders exists
if os.path.exists(PathToZipInput):
    print
    print("Found zip file: \n\t%s"%(PathToZipInput))
    # Is the subject in the system?
    if (not os.path.exists(RawMRIFolder)) & (not os.path.exists(ProcMRIFolder)) :
        print
        print("Subject: %s is not in the system yet!"%(Subid))
        print
        if (not os.path.exists(RawMRIFolder)):
            print("Found: %s"%(RawMRIFolder))
        # if (not os.path.exists(BehavDataFolder)):
        #     print("Found: %s"%(BehavDataFolder))
        if (not os.path.exists(ProcMRIFolder)):
            print("Found: %s"%(ProcMRIFolder))
        print("Subject %s is being entered"%(Subid))
        # Make subject/session folder in 
        # RawMRIData
        os.mkdir(RawMRIFolder)
        print("Made folder: %s"%(RawMRIFolder))
        # # BehavioralData
        # os.mkdir(BehavDataFolder)
        # print("Made folder: %s"%(BehavDataFolder))        
        # ProcessedMRIData
        os.mkdir(ProcMRIFolder)
        print("Made folder: %s"%(ProcMRIFolder))
    else:
        print("This subject is already in the system")

    # Is the visit in the system?
    if (not os.path.exists(VisRawMRIFolder)) & (not os.path.exists(VisProcMRIFolder)):
        print
        print("Visit: %s is not in the system yet!"%(Visitid))
        print
        if (not os.path.exists(VisRawMRIFolder)):
            print("Found: %s"%(VisRawMRIFolder))
        # if (not os.path.exists(VisBehavDataFolder)):
        #     print("Found: %s"%(VisBehavDataFolder))
        if (not os.path.exists(VisProcMRIFolder)):
            print("Found: %s"%(VisProcMRIFolder))
        print("Visit %s is being entered"%(Visitid))
        # RawMRIData
        os.mkdir(VisRawMRIFolder)
        print("Made folder: %s"%(VisRawMRIFolder))        
        # # BehavioralData
        # os.mkdir(VisBehavDataFolder)        
        # print("Made folder: %s"%(VisBehavDataFolder))
        # ProcessedMRIData
        os.mkdir(VisProcMRIFolder)        
        print("Made folder: %s"%(VisProcMRIFolder))
    # move ZIP file
        print("Working with zip file: %s"%(PathToZipInput))
        ZipFileName = os.path.basename(PathToZipInput)
        ZipFileOut = os.path.join(VisRawMRIFolder,ZipFileName)
        print("%s"%(ZipFileName))
        shutil.move(PathToZipInput,ZipFileOut)
    # unzip file
        # What is the extension?
        ZipExt = os.path.splitext(ZipFileOut)[-1]
        if ZipExt == ".gz":
            print("Unzipping with gunzip")
            os.system("gunzip %s -d %s"%(ZipFileOut,os.path.dirname(ZipFileOut)))
        elif ZipExt == ".zip":
            print("Unzipping with unzip")
            os.system("unzip %s -d %s"%(ZipFileOut,os.path.dirname(ZipFileOut)))
    # Un tar the file
        TarFileName = os.path.splitext(ZipFileName)[0]
        os.system("tar xvf %s --directory %s"%(os.path.join(VisRawMRIFolder,TarFileName),VisRawMRIFolder))
    # remove tar file
        os.remove(os.path.join(VisRawMRIFolder,TarFileName))
    # What is the name of the folder created after extracting the zip file?
        CreatedZipFolder = os.path.join(VisRawMRIFolder,os.listdir(VisRawMRIFolder)[0])
        print("Created this folder from the Zip file: \n\t%s"%(CreatedZipFolder))

    # reconstruct data
        LogFileLocation = os.path.join(VisRawMRIFolder, 'ReconstructionLog.txt')
        #os.system("/Applications/mricron/dcm2nii -d N -e Y -f N -g N -i N -n Y -o %s %s"%(VisRawMRIFolder,os.path.join(VisRawMRIFolder,os.path.basename(sys.argv[3]).split('.')[0])))
        os.system("/usr/bin/dcm2nii -d N -e Y -f N -g N -i N -n Y -t Y -o %s %s > %s"%(VisRawMRIFolder,CreatedZipFolder, LogFileLocation))
        #os.system("/Applications/MRIcron/dcm2nii -d N -e Y -f N -g N -i N -n Y -t Y -o %s %s"%(VisRawMRIFolder,CreatedZipFolder))
    else:
        print("This visit is already in the system")
        if (not os.path.exists(VisRawMRIFolder)):
            print("Found: %s"%(VisRawMRIFolder))
        # if (not os.path.exists(VisBehavDataFolder)):
        #     print("Found: %s"%(VisBehavDataFolder))
        if (not os.path.exists(VisProcMRIFolder)):
            print("Found: %s"%(VisProcMRIFolder))
else:
    print
    print("CANNOT find zip file: %s"%(sys.argv[3]))
    