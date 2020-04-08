import sys
import os
import shutil
from PyQt4.QtGui import *
# from NCM002_Import_Config import *


def main():
    MoveAllFiles(AllImports, RawMRIFolder, VisProcMRIFolder, PartID, Visitid)
    
def MoveAllFiles(AllImports, RawMRIFolder, VisProcMRIFolder, PartID, Visitid):
    for i in AllImports:
        # Ask the user to select the files according to the config file
        filename = SelectOneFile(i, RawMRIFolder)
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
    w = QFileDialog()
    # Set window size.
    w.resize(320, 240)
    # Set window title
    w.setWindowTitle("Hello World!")    
    title = 'Select the %s file'%(InputDict['Name'])
    filter = '%s(*%s*.%s)'%(InputDict['FileNameTag'],InputDict['SearchString'],InputDict['Extension'])
    filename = QFileDialog.getOpenFileName(w, title, RawMRIFolder, filter)
    return filename