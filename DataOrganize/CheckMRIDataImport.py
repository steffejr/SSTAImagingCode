import os
import sys
import shutil
import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
import pandas as pd
from PyQt4.QtGui import *
import pathlib
_thisDir = os.path.dirname(os.path.abspath(__file__))
# # import parameters from a config file
sys.path.append(os.path.join(_thisDir))
from NCM002_Import_Config import *
print('%s\n'%(LabName))

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
            # Add functionality for what to do if it is missing!
            FoundFlag.append(0)
    return FoundFlag

def FindMissingData(PartID, Visitid):
    # Got to the subject's raw data folder and see if the NII file exists. 
    # Check to see if the Proc folder exists
    
    pass
        
def MakeListOfImportFiles(AllImports):
    # Make the column names for the table of found data
    ImportList = []
    ImportList.append('PartID')
    ImportList.append('Visitid')    
    for i in AllImports:
        ImportList.append(i['FileNameTag'] + '_' + i['Extension'])
    return ImportList
        
# if __name__ == "__main__":
#     BaseDir = MRIDataImport.FindBaseDirectory(LabName, StudyName, DataPath)
#     df = MakeListOfAllParticipants(BaseDir, AllImports)
#     OutFileName = os.path.join(os.path.split(BaseDir)[0:-1][0],'SummaryData','MRIProcDataStatus.csv')
#     df.to_csv(OutFileName)    
# #     main()
