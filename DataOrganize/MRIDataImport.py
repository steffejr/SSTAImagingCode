import os
import sys
import shutil
import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *

from PyQt5.QtWidgets import *
import pathlib
_thisDir = os.path.dirname(os.path.abspath(__file__))
# import parameters from a config file
sys.path.append(os.path.join(_thisDir))
from NCM002_Import_Config import *
DataPath

def main():

    # Find the base directory for data storage
    print("Lab name: %s"%(LabName))
    print("Study name: %s"%(StudyName))
    print("Data Path: %s"%(DataPath))    
    BaseDir = FindBaseDirectory(LabName, StudyName, DataPath)
    # Find the participant ID
    PartID, Visitid = GetParticipantID()
    Visitid = "V%03d"%(int(Visitid)) 
    # What are the data folders?
    RawMRIFolder, ProcMRIFolder, VisRawMRIFolder, VisProcMRIFolder = DataFolders(BaseDir, PartID, Visitid)
    # Check to see if this participant is already in the system
    success = CheckIfParticipantIsInSystem(RawMRIFolder, ProcMRIFolder, PartID)
    # Ask the user if they want to continue if this part is in the system
    if not success:
        response = messagebox.askyesno('Participant: %s'%(PartID),'This participant is already in system. Do you want to continue?')
        if not response:
            return
    # Check to see if this VISIT is already in the system
    success = CheckIfVisitIsInSystem(VisRawMRIFolder, VisProcMRIFolder, PartID)
    # Ask the user if they want to continue if this part is in the system
    if not success:
        response = messagebox.askyesno('Participant: %s, Visit: %s'%(PartID, Visitid),'This VISIT is already in system. Do you want to continue?')
        if not response:
            return
    # # Should previously reconstructed data be overwritten?
    # OverWriteFlag = messagebox.askyesno('Overwrite','When reconstructing data should existing data be overwritten?')
    # if OverWriteFlag:
    #     OverWriteFlag = messagebox.askyesno('Sure?','Are you sure you want to overwrite?')
    # if OverWriteFlag:
    #     print('Existing data will be overwritten')
        
    # Take an already reconstructed data set in the Raw folder and rename and copy 
    # any missing files to the Proc folder
    
    
    # Find the zip file of data
    PathToZipInput = PickZipdataFile()
    # Add a check here. If the user does NOT pick a zip file the program can check 
    # to see if the raw data was already downloaded and unzipped.
    # It is possible that we may wish to simply re-reconstruct the raw data
    # Move the zip file
    if len(PathToZipInput) > 0:
        print('Path to zip file: %s'%(PathToZipInput))
        PathToZipInput = MoveZipFile(PathToZipInput, VisRawMRIFolder)

        # Unzip the daPathToZipInputta file
        UnZipData(PathToZipInput)
        # untar the data file
        CreatedDataFolder = UnTarData(VisRawMRIFolder, PathToZipInput)
    else:
        CreatedDataFolder = os.path.join(VisRawMRIFolder,os.listdir(VisRawMRIFolder)[0])
    # reconstruct the data
    ReconstructMRIData(VisRawMRIFolder, CreatedDataFolder)
    # Rename and move all files
    MoveAllFiles(AllImports, RawMRIFolder, VisProcMRIFolder, PartID, Visitid)
    # Make the stats and extra folders as specified in the config file
    MakeStatsFolders(VisProcMRIFolder)
    messagebox.showinfo('Done','All Done with: %s, %s'%(PartID, Visitid))
    
def FindBaseDirectory(LabName, StudyName, DataPath):
    # Now find the Base folder
    # First, split the path
    splitThisScript = DataPath.split(os.path.sep)
    # Find where the lab name is
    # This also works if the lab name is in tha path name more then once. If so 
    # the last time it appears is used.
    indices = [i for i, x in enumerate(splitThisScript) if x == LabName]
    BaseDir = os.path.join(*splitThisScript[0:indices[-1]+1])
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
    return PathToZipInput

def MoveZipFile(PathToZipInput, VisRawMRIFolder):
    # move ZIP file
    print("Working with zip file: %s"%(PathToZipInput))
    ZipFileName = os.path.basename(PathToZipInput)
    ZipFileOut = os.path.join(VisRawMRIFolder,ZipFileName)
    print("%s"%(ZipFileName))
    shutil.copy(PathToZipInput,ZipFileOut)    
    return ZipFileOut 
    
def DataFolders(BaseDir, Subid, Visitid):
    RawMRIFolder = os.path.join(BaseDir,"RawMRIData",Subid)
#    BehavDataFolder = os.path.join(BaseDir,"BehavioralData",Subid)        
    ProcMRIFolder = os.path.join(BaseDir,"ProcMRIData",Subid)

    VisRawMRIFolder = os.path.join(BaseDir,"RawMRIData",Subid,Visitid)
#    VisBehavDataFolder = os.path.join(BaseDir,"BehavioralData",Subid,Visitid)        
    VisProcMRIFolder = os.path.join(BaseDir,"ProcMRIData",Subid,Visitid)
    print(VisProcMRIFolder)
    return RawMRIFolder, ProcMRIFolder, VisRawMRIFolder, VisProcMRIFolder

def ReconstructMRIData(VisRawMRIFolder, CreatedZipFolder):
    print('Reconstructing data...')
    LogFileLocation = os.path.join(VisRawMRIFolder, 'ReconstructionLog.txt')
    #os.system("/Applications/mricron/ -d N -e Y -f N -g N -i N -n Y -o %s %s"%(VisRawMRIFolder,os.path.join(VisRawMRIFolder,os.path.basename(sys.argv[3]).split('.')[0])))
    print("%s -o %s %s > %s"%(dcm2niiPath, VisRawMRIFolder,CreatedZipFolder, LogFileLocation))
    os.system("%s -o %s %s > %s"%(dcm2niiPath, VisRawMRIFolder,CreatedZipFolder, LogFileLocation))
    
def UnTarData(VisRawMRIFolder, ZipFileName):
    # Un tar the file
    TarFileName = os.path.splitext(ZipFileName)[0]
    os.system("tar xvf %s --directory %s"%(os.path.join(VisRawMRIFolder,TarFileName),VisRawMRIFolder))
    # remove tar file
    os.remove(os.path.join(VisRawMRIFolder,TarFileName))
    # What is the name of the folder created after extracting the zip file?
    CreatedDataFolder = os.path.join(VisRawMRIFolder,os.listdir(VisRawMRIFolder)[0])
    print("Created this folder from the Zip file: \n\t%s"%(CreatedDataFolder))
    return CreatedDataFolder
    
def UnZipData(PathToZipInput):
# unzip file
    # What is the extension?
    ZipExt = os.path.splitext(PathToZipInput)[-1]
    if ZipExt == ".gz":
        print("Unzipping with gunzip")
        os.system("gunzip %s -d %s"%(PathToZipInput,os.path.dirname(PathToZipInput)))
    elif ZipExt == ".zip":
        print("Unzipping with unzip")
        os.system("unzip %s -d %s"%(PathToZipInput,os.path.dirname(PathToZipInput)))    

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
        os.mkdir(ProcMRIFolder)
        print("Made folder: %s"%(ProcMRIFolder))
    else:
        # message = messagebox.showwarning("Warning","This subject is already in the system")
        success = False
    return success

def CheckIfVisitIsInSystem(VisRawMRIFolder, VisProcMRIFolder, VisitID):
    success = True
    if (not os.path.exists(VisRawMRIFolder)) & (not os.path.exists(VisProcMRIFolder)) :
        print
        print("Visit: %s is not in the system yet!"%(VisitID))
        # Make subject/session folder in 
        # RawMRIData
        os.mkdir(VisRawMRIFolder)
        print("Made folder: %s"%(VisRawMRIFolder))
        os.mkdir(VisProcMRIFolder)
        print("Made folder: %s"%(VisProcMRIFolder))
    else:
        # message = messagebox.showwarning("Warning","This VISIT is already in the system")
        success = False
    return success

# def MoveFile(FilePath, VisProcMRIFolder, Subid, Visitid, Type, Ext = 'nii'):
#     # make the folder
#     # make new name
# 
#     OutName = "%s_%s_%s.%s"%(Subid,Visitid,Type, Ext)
#     os.mkdir(os.path.join(VisProcMRIFolder,Type))
#     os.mkdir(os.path.join(VisProcMRIFolder,Type,ProcessedNIIFileFolderName))
#     shutil.copy(FilePath,os.path.join(VisProcMRIFolder,Type,OutName))
#     shutil.copy(FilePath,os.path.join(VisProcMRIFolder,Type,ProcessedNIIFileFolderName,OutName))

def NIIFile():
    # Ask the user to select the zip file
    PathToZipInput = askopenfilename(title='Select *.tar.gz file', initialdir = '~/Downloads', filetypes = [('NII files','*DMS*.nii')])
    return PathToZipInput

    
def MoveAllFiles(AllImports, RawMRIFolder, VisProcMRIFolder, PartID, Visitid):
    for i in AllImports:
        # Ask the user to select the files according to the config file
        filename = SelectOneFile(RawMRIFolder, i)
        if len(filename) > 0:
            # Create the name of the file
            OutFileName =  "%s_%s_%s.%s"%(PartID,Visitid,i['FileNameTag'], i['Extension'])
            # Create the output path for the file
            # Add another parameter to the AllImports structure naming the ouput folder
            # which allows multiple images to reconstruct to the same folder
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
    print('=================================================')
    print('=================================================')
    print('Tag is %s.\n\tFile selected is:\n\t\t%s'%(Tag, InFilePath))
    print('-------------------------------------------------')    
    for folder in Folders:
        if not os.path.exists(folder):
            os.mkdir(folder)
        else:
            print('Folder: %s already exists'%(folder))
            print('-------------------------------------------------')    
    # Copy the file
    shutil.copy(InFilePath, os.path.join(OutFilePath, OriginalNIIFileFolderName, OutFileName))
    shutil.copy(InFilePath, os.path.join(OutFilePath, ProcessedNIIFileFolderName, OutFileName))

def SelectOneFile(RawMRIFolder, InputDict):
    """
    Select a file via a dialog and return the file name.
    """
    try:
        from PyQt5.QtWidgets import QApplication, QFileDialog
    except ImportError:
        try:
            from PyQt4.QtGui import QApplication, QFileDialog
        except ImportError:
            from PySide.QtGui import QApplication, QFileDialog


    title = 'Select the %s file'%(InputDict['Name'])
    TypeFilter = '%s(*%s*.%s)'%(InputDict['FileNameTag'],InputDict['SearchString'],InputDict['Extension'])
    TypeFilter = '*%s*.%s'%(InputDict['SearchString'],InputDict['Extension'])
    #TypeFilter = '*asl*.nii'
    print("On a MAC the title is not shown on the selection box!")
    print(title)
    print(TypeFilter)
    app = QApplication([RawMRIFolder])
    fname = QFileDialog.getOpenFileName(None, title,
                                        RawMRIFolder, filter=TypeFilter)
    if isinstance(fname, tuple):
        return fname[0]
    else:
        return str(fname) 
    

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

if __name__ == "__main__":
     main()

