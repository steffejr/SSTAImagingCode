import os
import sys
import shutil
import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from pathlib import Path
from PyQt4.QtGui import *

# __file__ = Path('/Volumes/GoogleDrive/Shared drives/NCMLab/Scripts/Imaging/DataOrganize/MRI.py')

# The Path is an updated object orietned way to use paths
ThisFile = Path(__file__)
print("This file is:")
print(ThisFile)

_thisDir = ThisFile.parents[0]# os.path.dirname(os.path.abspath(__file__))
# import parameters from a config file
sys.path.append(str(_thisDir))
#
from NCM002_Import_Config import *

def main():

    # Find the base directory for data storage
    BaseDir = FindBaseDirectory(LabName, StudyName)
    # Find the participant ID
    PartID, Visitid = GetParticipantID()
    Visitid = "V%03d"%(int(Visitid)) 
    # What are the data folders?
    RawMRIFolder, ProcMRIFolder, VisRawMRIFolder, VisProcMRIFolder = DataFolders(BaseDir, PartID, Visitid)
    # Check to see if this participant is already in teh system
    success = CheckIfParticipantIsInSystem(RawMRIFolder, ProcMRIFolder, PartID)
    # Ask the user if they want to continue if this part is in the system
    if not success:
        response = messagebox.askyesno('Partcipant: %s'%(PartID),'This participant is already in system. Do you want to continue?')
        if not response:
            return
    # Check to see if this VISIT is already in teh system
    success = CheckIfVisitIsInSystem(VisRawMRIFolder, VisProcMRIFolder, PartID)
    # Ask the user if they want to continue if this part is in the system
    if not success:
        response = messagebox.askyesno('Partcipant: %s, Visit: %s'%(PartID, Visitid),'This VISIT is already in system. Do you want to continue?')
        if not response:
            return

    # Find the zip file of data
    PathToZipInput = PickZipdataFile()
    # Move the zip file
    PathToZipInput = MoveZipFile(PathToZipInput, VisRawMRIFolder)
    # Unzip the data file
    UnZipData(PathToZipInput)
    # untar the data file
    CreatedDataFolder = UnTarData(VisRawMRIFolder, PathToZipInput)
    # reconstruct the data
    ReconstructMRIData(VisRawMRIFolder, CreatedDataFolder)
    # Rename and move all files
    MoveAllFiles(AllImports, RawMRIFolder, VisProcMRIFolder, PartID, Visitid)
    # Make the stats and extra folders as specified in the config file
    MakeStatsFolders(VisProcMRIFolder)
    messagebox.showinfo('Done','All Done with: %s, %s'%(PartID, Visitid))
    
def FindBaseDirectory(LabName, StudyName):
    # Start with this script's folder
    ThisScript = os.path.dirname(os.path.realpath(__file__))
    # Now find the Base folder
    # First, split the path
    splitThisScript = ThisScript.split(os.path.sep)
    # Find where the lab name is
    ind = splitThisScript.index(LabName)
    BaseDir = os.path.join(*splitThisScript[0:ind+1])
    BaseDir = os.path.join(os.path.sep, BaseDir, StudyName, 'Data', 'Imaging')
    return BaseDir
    
def GetParticipantID():
    application_window = tk.Tk()
    application_window.withdraw()
    PartID = simpledialog.askstring("Input", "What is the participant ID?",
                                parent=application_window)

    VisitID = simpledialog.askinteger("Input", "What is the visit ID?",
                                 parent=application_window,
                                 minvalue=0, maxvalue=10)
    application_window.destroy()
    return PartID, VisitID
    
def PickZipdataFile():
    application_window = tk.Tk()
    application_window.withdraw()
    # Ask the user to select the zip file
    # PathToZipInput = askopenfilename(title='Select *.tar.gz file', initialdir = '~/Downloads', filetypes = [('Zipped files','*.tar.gz')], parent=application_window)
    PathToZipInput = askopenfilename(title='Select *.tar.gz file', initialdir = '~/Downloads', parent=application_window)
    application_window.destroy()
    # Change type to Path
    PathToZipInput = Path(PathToZipInput)
    return PathToZipInput

def MoveZipFile(PathToZipInput, VisRawMRIFolder):
    # move ZIP file
    print("Working with zip file: %s"%(PathToZipInput))
        
    ZipFileName = PathToZipInput.name # os.path.basename(PathToZipInput)
    ZipFileOut = Path(VisRawMRIFolder)/ZipFileName
    # ZipFileOut = os.path.join(VisRawMRIFolder,ZipFileName)
    print("%s"%(ZipFileName))
    shutil.copy(str(PathToZipInput), str(ZipFileOut))    
    return ZipFileOut 
    
def DataFolders(BaseDir, PartID, Visitid):
    # This is now using Path 
    RawMRIFolder = Path(BaseDir)/"RawData"/PartID # os.path.join(BaseDir,"RawMRIData",PartID)
#    BehavDataFolder = os.path.join(BaseDir,"BehavioralData",Subid)        
    ProcMRIFolder = Path(BaseDir)/"ProcMRIData"/PartID # os.path.join(BaseDir,"ProcMRIData",PartID)

    VisRawMRIFolder = Path(BaseDir)/"RawMRIData"/PartID/Visitid # os.path.join(BaseDir,"RawMRIData",PartID,Visitid)
#    VisBehavDataFolder = os.path.join(BaseDir,"BehavioralData",Subid,Visitid)        
    VisProcMRIFolder = Path(BaseDir)/"ProcMRIData"/PartID/Visitid # os.path.join(BaseDir,"ProcMRIData",PartID,Visitid)
    print(VisProcMRIFolder)
    return RawMRIFolder, ProcMRIFolder, VisRawMRIFolder, VisProcMRIFolder

def ReconstructMRIData(VisRawMRIFolder, CreatedZipFolder):
    LogFileLocation = Path(VisRawMRIFolder)/'ReconstructionLog.txt' # os.path.join(VisRawMRIFolder, 'ReconstructionLog.txt')
    #os.system("/Applications/mricron/dcm2nii -d N -e Y -f N -g N -i N -n Y -o %s %s"%(VisRawMRIFolder,os.path.join(VisRawMRIFolder,os.path.basename(sys.argv[3]).split('.')[0])))
    os.system("/usr/bin/dcm2nii -d N -e Y -f N -g N -i N -n Y -t Y -o %s %s > %s"%(VisRawMRIFolder,CreatedZipFolder, LogFileLocation))
    
def UnTarData(VisRawMRIFolder, ZipFileName):
    # Un tar the file
    TarFileName = ZipFileName.name # os.path.splitext(ZipFileName)[0]
    os.system("tar xvf %s --directory %s"%(str(Path(VisRawMRIFolder)/TarFileName),VisRawMRIFolder))
    tar = tarfile.open(fname, "r:gz")
    tar.extractall()
    tar.close()
    tar = tarfile.open((VisRawMRIFolder/TarFileName), "r:gz")
    tar.extractall()
    tar.close()
#    os.system("tar xvf %s --directory %s"%(os.path.join(VisRawMRIFolder,TarFileName),VisRawMRIFolder))
    # remove tar file
    temp = Path(VisRawMRIFolder)/TarFileName
    temp.unlink()
    # os.remove(os.path.join(VisRawMRIFolder,TarFileName))
    # What is the name of the folder created after extracting the zip file?
    temp = os.listdir(str(VisRawMRIFolder))[0]
    CreatedDataFolder = Path(VisRawMRIFolder)/temp
    # CreatedDataFolder = os.path.join(VisRawMRIFolder,os.listdir(VisRawMRIFolder)[0])
    print("Created this folder from the Zip file: \n\t%s"%(CreatedDataFolder))
    return CreatedDataFolder
    
def UnZipData(PathToZipInput):
# unzip file
    # Check to see if there is a space in teh file name
    # What is the extension?
    ZipExt = PathToZipInput.suffix # os.path.splitext(PathToZipInput)[-1]
    if ZipExt == ".gz":
        print("Unzipping with gunzip")
        os.system("gunzip %s -d %s"%(str(PathToZipInput), PathToZipInput.parent)) # os.path.dirname(PathToZipInput)))
    elif ZipExt == ".zip":
        print("Unzipping with unzip")
        os.system("unzip %s -d %s"%(str(PathToZipInput), PathToZipInput.parent)) #os.path.dirname(PathToZipInput)))    

def MakeDataFolders(VisRawMRIFolder, VisProcMRIFolder):                
    if (not os.path.exists(VisRawMRIFolder)):
        print("Found: %s"%(VisRawMRIFolder))
    # if (not os.path.exists(VisBehavDataFolder)):
    #     print("Found: %s"%(VisBehavDataFolder))
    if (not os.path.exists(VisProcMRIFolder)):
        print("Found: %s"%(VisProcMRIFolder))
    # print("Visit %s is being entered"%(Visitid))
    # RawMRIData
    os.mkdir(VisRawMRIFolder)
    print("Made folder: %s"%(VisRawMRIFolder))        

    os.mkdir(VisProcMRIFolder)        
    print("Made folder: %s"%(VisProcMRIFolder))        
    # Make folder for processed data
    
    
def CheckIfParticipantIsInSystem(RawMRIFolder, ProcMRIFolder, Subid):
    success = True
    if (not RawMRIFolder.exists()) & (not ProcMRIFolder.exists()) :
    # if (not os.path.exists(RawMRIFolder)) & (not os.path.exists(ProcMRIFolder)) :
        print
        print("Subject: %s is not in the system yet!"%(Subid))
        print
        if (not RawMRIFolder.exists()):        
        # if (not os.path.exists(RawMRIFolder)):
            print("Found: %s"%(RawMRIFolder))
        # if (not os.path.exists(BehavDataFolder)):
        #     print("Found: %s"%(BehavDataFolder))
        if (not ProcMRIFolder.exists()):
        # if (not os.path.exists(ProcMRIFolder)):
            print("Found: %s"%(ProcMRIFolder))
        print("Subject %s is being entered"%(Subid))
        # Make subject/session folder in 
        # RawMRIData
        RawMRIFolder.mkdir()
        # os.mkdir(RawMRIFolder)
        print("Made folder: %s"%(RawMRIFolder))
        ProcMRIFolder.mkdir()
        # os.mkdir(ProcMRIFolder)
        print("Made folder: %s"%(ProcMRIFolder))
    else:
        # message = messagebox.showwarning("Warning","This subject is already in the system")
        success = False
    return success

def CheckIfVisitIsInSystem(VisRawMRIFolder, VisProcMRIFolder, VisitID):
    success = True
    if (not VisRawMRIFolder.exists()) & (not VisProcMRIFolder.exists()) :
    # if (not os.path.exists(VisRawMRIFolder)) & (not os.path.exists(VisProcMRIFolder)) :
        print
        print("Visit: %s is not in the system yet!"%(VisitID))
        # Make subject/session folder in 
        # RawMRIData
        VisRawMRIFolder.exists()
        # os.mkdir(VisRawMRIFolder)
        print("Made folder: %s"%(VisRawMRIFolder))
        VisProcMRIFolder.exists()
        # os.mkdir(VisProcMRIFolder)
        print("Made folder: %s"%(VisProcMRIFolder))
    else:
        # message = messagebox.showwarning("Warning","This VISIT is already in the system")
        success = False
    return success

def MoveFile(FilePath, VisProcMRIFolder, Subid, Visitid, Type, Ext = 'nii'):
    # make the folder
    # make new name

    OutName = "%s_%s_%s.%s"%(Subid,Visitid,Type, Ext)
    os.mkdir(os.path.join(VisProcMRIFolder,Type))
    os.mkdir(os.path.join(VisProcMRIFolder,Type,ProcessedNIIFileFolderName))
    shutil.copy(FilePath,os.path.join(VisProcMRIFolder,Type,OutName))
    shutil.copy(FilePath,os.path.join(VisProcMRIFolder,Type,ProcessedNIIFileFolderName,OutName))

def NIIFile():
    # Ask the user to select the zip file
    PathToZipInput = askopenfilename(title='Select *.tar.gz file', initialdir = '~/Downloads', filetypes = [('NII files','*DMS*.nii')])
    return PathToZipInput

    
def MoveAllFiles(AllImports, RawMRIFolder, VisProcMRIFolder, PartID, Visitid):
    for i in AllImports:
        # Ask the user to select the files according to the config file
        filename = SelectOneFile(i, RawMRIFolder)
        if len(filename) > 0:
            # Create the name of the file
            OutFileName =  "%s_%s_%s.%s"%(PartID,Visitid,i['FileNameTag'], i['Extension'])
            # Create the output path for the file
            OutFilePath = os.path.join(VisProcMRIFolder, i['FileNameTag'])
            MoveFile(filename, OutFileName, OutFilePath, i['FileNameTag'])

    
def MoveFile(InFilePath, OutFileName, OutFilePath, Tag):
    # make the folders
    # If the folder already exists do not make a new one
    # Create a list of folder paths to check for
    Folders = []
    Folders.append(OutFilePath)
    Folders.append(os.path.join(OutFilePath, OriginalNIIFileFolderName))
    Folders.append(os.path.join(OutFilePath, ProcessedNIIFileFolderName))
    for folder in Folders:
        if not os.path.exists(folder):
            os.mkdir(folder)
        else:
            print('Folder: %s already exists'%(folder))
    # Copy the file
    shutil.copy(InFilePath, os.path.join(OutFilePath, OriginalNIIFileFolderName, OutFileName))
    shutil.copy(InFilePath, os.path.join(OutFilePath, ProcessedNIIFileFolderName, OutFileName))
    
def SelectOneFile(InputDict, RawMRIFolder):     
    a = QApplication(sys.argv)
    w = QFileDialog()
    # Set window size.
    w.resize(320, 240)
    # Set window title
    w.setWindowTitle("Hello World!")    
    title = 'Select the %s file'%(InputDict['Name'])
    FileFilter = '%s(*%s*.%s)'%(InputDict['FileNameTag'],InputDict['SearchString'],InputDict['Extension'])
    filename = QFileDialog.getOpenFileName(w, title, RawMRIFolder, FileFilter)
    return filename

def MakeStatsFolders(VisProcMRIFolder):
    os.mkdir(os.path.join(VisProcMRIFolder, 'fMRIStats'))
    # Make additional folders for holding stat results        
    for folderName in StatsFoldersList:
        tempFolder = os.path.join(VisProcMRIFolder, 'fMRIStats',folderName)
        if not os.path.exists(tempFolder):
            os.mkdir(tempFolder)
            os.mkdir(os.path.join(tempFolder, 'Model1'))
        else:
            print('Folder: %s already exists'%(tempFolder))
    for folderName in ExtraFolders:
        tempFolder = os.path.join(VisProcMRIFolder, folderName)
        if not os.path.exists(tempFolder):
            os.mkdir(tempFolder)
        else:
            print('Folder: %s already exists'%(tempFolder))
# 
# if __name__ == "__main__":
#     main()

