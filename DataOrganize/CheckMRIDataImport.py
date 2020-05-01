import os
import sys
import shutil
import glob
import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
import pandas as pd
from PyQt4.QtGui import *
import datetime
import pathlib
_thisDir = os.path.dirname(os.path.abspath(__file__))
# # import parameters from a config file
sys.path.append(os.path.join(_thisDir))
from NCM002_Import_Config import *
print('%s\n'%(LabName))
print(DataPath)
import MRIDataImport

def main():
    # Find the base directory for data storage
    BaseDir = MRIDataImport.FindBaseDirectory(LabName, StudyName, DataPath)
    # Find the participant ID
    PartID, Visitid = MRIDataImport.GetParticipantID()
    Visitid = "V%03d"%(int(Visitid)) 
    # What are the data folders?
    RawMRIFolder, ProcMRIFolder, VisRawMRIFolder, VisProcMRIFolder = MRIDataImport.DataFolders(BaseDir, PartID, Visitid)
    # Check to see if this participant is already in the system
    success = MRIDataImport.CheckIfParticipantIsInSystem(RawMRIFolder, ProcMRIFolder, PartID)
    # Ask the user if they want to continue if this part is in the system
    if not success:
        response = messagebox.askyesno('Participant: %s'%(PartID),'This participant is already in system. Do you want to continue?')
        if not response:
            return
    # Check to see if this VISIT is already in the system
    success = MRIDataImport.CheckIfVisitIsInSystem(VisRawMRIFolder, VisProcMRIFolder, PartID)
    # Ask the user if they want to continue if this part is in the system
    if not success:
        response = messagebox.askyesno('Participant: %s, Visit: %s'%(PartID, Visitid),'This VISIT is already in system. Do you want to continue?')
        if not response:
            return
    # Cycle over each folder for this participant and check to see if everything 
    # is where it is expected

def MakeListOfAllParticipants(BaseDir, AllImports):
    # Cycle over all participant folders and check to see what has been reconstructed and 
    # is in each participant's ProcData folder
    # Make a table of data 
    df = pd.DataFrame(columns = MakeListOfImportFiles(AllImports))
    Visitid = 'V001'
    # What is the Proc data folder
    ProcMRIFolderAllPart = os.path.join(BaseDir, 'ProcMRIData')
    # Make list of all Part 
    AllPartList = [dI for dI in os.listdir(ProcMRIFolderAllPart) if os.path.isdir(os.path.join(ProcMRIFolderAllPart,dI))]
    for CurrentPart in AllPartList:
        if (CurrentPart[0] == '1') or (CurrentPart[0] == '2'):
            print('Found one: %s'%(CurrentPart))
            VisProcMRIFolder = os.path.join(BaseDir,"ProcMRIData",CurrentPart,Visitid)
            NewData = pd.Series(CheckAllFiles(AllImports, VisProcMRIFolder, CurrentPart, Visitid), index = df.columns)
            df = df.append(NewData, ignore_index = True)
    return df
        
def CheckAllFiles(AllImports, VisProcMRIFolder, PartID, Visitid):
    # Cycle over the list of all data to import and check to see if the participant
    # has the data
    FoundFlag = []
    FoundFlag.append(PartID)
    FoundFlag.append(Visitid)    
    for i in AllImports:
        # Ask the user to select the files according to the config file
        OutFileName =  "%s_%s_%s.%s"%(PartID,Visitid,i['FileNameTag'], i['Extension'])
        # Create the output path for the file
        OutFilePath = os.path.join(VisProcMRIFolder, i['FileNameTag'],OriginalNIIFileFolderName)
        ExpectedFilePath = os.path.join(OutFilePath, OutFileName)    
        # Does this file exist?
        if os.path.exists(ExpectedFilePath):
            FoundFlag.append(1)
        else:
            # If it is not in the Proc folder, check to see if there is anythin 
            # in the Raw data folder
            RawMRIFolder = os.path.join(BaseDir,"RawMRIData",PartID,Visitid)
        
            # Add functionality for what to do if it is missing!
            FoundFlag.append(0)
            print('%s Missing file: %s'%(PartID,OutFileName))            
            # If a file is found to be missing, check to see if it is sitting in teh Raw data folder.
            FoundFiles = glob.glob(os.path.join(RawMRIFolder, '*'+i['SearchString']+'*.nii'))            
            if len(FoundFiles) > 0:
                print('\t Found a raw copy of it')
                FindAndMoveFile(i, BaseDir, PartID, Visitid,VisProcMRIFolder)
            elif i['Extension'] == 'nii':
                print('\tLooking for Raw DICOM')
                FindReconSingleDICOM(RawMRIFolder, i)
                FoundFiles = glob.glob(os.path.join(RawMRIFolder, '*'+i['SearchString']+'*.nii'))            
                if len(FoundFiles) > 0:
                    print('\t\tFound DICOM')
                    FindAndMoveFile(i, BaseDir, PartID, Visitid,VisProcMRIFolder)
            else:
                print('\tDid not find raw copy or DICOM data')
    return FoundFlag

def WriteOutNewdataMoveOldData(UpdatedData, UpdatedDataFileName, ExistingDataFileName, AllOutDataFolder):
    # Move the old file 
    OldDataFolder = os.path.join(AllOutDataFolder, 'OldResultFiles')
    # if the folder for old data does not exist, then make it
    if not os.path.exists(OldDataFolder):
        os.mkdir(OldDataFolder)
    # change the name of the results file so it is not confused with current data
    MovedDataFile = os.path.join(OldDataFolder, 'X_'+os.path.basename(ExistingDataFileName))
    shutil.move(ExistingDataFileName, MovedDataFile)
    # Now that the old data is moved, write out the updated data
    UpdatedData.to_csv(UpdatedDataFileName, index = False, float_format='%.3f')    
        
def LocateOutDataFile(BaseFileName, AllOutDataFolder):
    # Locate an existing processed data file and if it does not exist, then make it.
    # What files exist with this name?
    Files = glob.glob(os.path.join(AllOutDataFolder, BaseFileName + '*.csv'))
    now = datetime.datetime.now()
    NowString = now.strftime("_updated_%b-%d-%Y_%H-%M.csv")
    NewOutFileName = BaseFileName + NowString
    if len(Files) == 0:
        FileName = os.path.join(AllOutDataFolder, NewOutFileName)
    else:
        # this will open an existing file
        FileName = Files[-1] 
    return FileName

def LoadOutDataFile(OutDataFilePathName):
    # Make a data frame from CSV file
    OutDF = pd.read_csv(OutDataFilePathName)
    return OutDF   

def CreateOutFileName(AllOutDataFolder, BaseFileName):
# Create a file to hold processed data using the time and date
# to indicate when it was made
    now = datetime.datetime.now()
    NowString = now.strftime("_updated_%b-%d-%Y_%H-%M.csv")
    NewOutFileName = os.path.join(AllOutDataFolder, BaseFileName + NowString)
    return NewOutFileName
                                                
def MakeListOfImportFiles(AllImports):
    # Make the column names for the table of found data
    ImportList = []
    ImportList.append('PartID')
    ImportList.append('Visitid')    
    for i in AllImports:
        ImportList.append(i['FileNameTag'] + '_' + i['Extension'])
    return ImportList
    
def FindAndMoveFile(i, BaseDir, PartID, Visitid,VisProcMRIFolder):
    RawMRIFolder = os.path.join(BaseDir,"RawMRIData",PartID,Visitid)
    filename = MRIDataImport.SelectOneFile(i, RawMRIFolder)
    if len(filename) > 0:
        # Create the name of the file
        OutFileName =  "%s_%s_%s.%s"%(PartID,Visitid,i['FileNameTag'], i['Extension'])
        # Create the output path for the file
        # Add another parameter to the AllImports structure naming the ouput folder
        # which allows multiple images to reconstruct to the same folder
        OutFilePath = os.path.join(VisProcMRIFolder, i['FileNameTag'])
        MRIDataImport.MoveFile(filename, OutFileName, OutFilePath, i['FileNameTag'])

def FindReconSingleDICOM(RawMRIFolder, Image):
    # Find teh Raw DICOM top level folder
    FoundFiles = glob.glob(os.path.join(RawMRIFolder,'JST*'))
    if len(FoundFiles) > 0:
        RawDICOMFolder = FoundFiles[0]
        # Now find the image of interest
        FoundFiles = glob.glob(os.path.join(RawDICOMFolder,'*'+Image['ReconPathName']+'*'))
        if len(FoundFiles) > 0:
            RawDICOMImageFolder = FoundFiles[0]
            LogFileLocation = os.path.join(RawMRIFolder, 'ReconstructionLog.txt')
            os.system("/usr/bin/dcm2nii -d N -e Y -f N -g N -i N -n Y -t Y -o %s %s > %s"%(RawMRIFolder,RawDICOMImageFolder, LogFileLocation))                
        else:
            print("Could not find Image DICOM data")
    else:
        print("Could not find this Participants' DICOM data")
#                                                     
if __name__ == "__main__":
    BaseDir = MRIDataImport.FindBaseDirectory(LabName, StudyName, DataPath)
    NewData = MakeListOfAllParticipants(BaseDir, AllImports)
    # Load old data
    BaseFileName = 'NCM_Master_MRIStatus'
    AllOutDataFolder = os.path.join(os.path.split(BaseDir)[0:-1][0],'SummaryData')
    ExistingDataFileName = LocateOutDataFile(BaseFileName, AllOutDataFolder)
    print(ExistingDataFileName)
    # Load the existing results file
    if os.path.exists(ExistingDataFileName):
        # # Found the existing data file
        OldData = LoadOutDataFile(ExistingDataFileName)
        # created an updated results datafram, respectivein the "locked down" 
        # data rows
        UpdatedData = CreateUpdatedDataFrameOfResults(NewData, OldData)
        # Create an updated output file name
        UpdatedDataFileName = CreateOutFileName(AllOutDataFolder,BaseFileName)
        # write out the updated data and move the old data file
        WriteOutNewdataMoveOldData(NewData, UpdatedDataFileName, ExistingDataFileName, AllOutDataFolder)   

    else:
        # There is no old data file
        OldData = []
        NewData.to_csv(ExistingDataFileName, index = False, float_format='%.3f')

# Locked down procedures...