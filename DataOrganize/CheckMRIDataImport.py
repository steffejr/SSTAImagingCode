import os
import sys
import shutil
import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *

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

def MakeListOfAllParticipants():
    # return PartList
    pass
    
def CheckAllParticipants():
    # Make a table of data 
    df = pd.DataFrame(columns = MakeListOfImportFiles(AllImports))
    # Add this subject df.append(pd.Series(name='9999'))
        
def CheckAllFiles(AllImports, RawMRIFolder, VisProcMRIFolder, PartID, Visitid):
    for i in AllImports:
        # Ask the user to select the files according to the config file
        OutFileName =  "%s_%s_%s.%s"%(PartID,Visitid,i['FileNameTag'], i['Extension'])
        # Create the output path for the file
        OutFilePath = os.path.join(VisProcMRIFolder, i['FileNameTag'],OriginalNIIFileFolderName)
        ExpectedFilePath = os.path.join(OutFilePath, OutFileName)    
        # Does this file exist?
        if os.path.exists(ExpectedFilePath):
            df = df.insert({'PartID': PartID, i['FileNameTag'] + '_' + i['Extension']: True},ignore_index = True)
        
def MakeListOfImportFiles(AllImports):
    ImportList = []
    ImportList.append('PartID')
    ImportList.append('Visitid')    
    for i in AllImports:
        ImportList.append(i['FileNameTag'] + '_' + i['Extension'])
    return ImportList
        
if __name__ == "__main__":
    main()
