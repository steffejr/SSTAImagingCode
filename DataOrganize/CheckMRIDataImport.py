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
    BaseDir = MRIDataImport.FindBaseDirectory(LabName, StudyName)
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

if __name__ == "__main__":
    main()
