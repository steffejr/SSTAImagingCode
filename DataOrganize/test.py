import os
from tkinter.filedialog import askopenfilename
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
# Find the folder for the raw MRI data
RawDataFolder = os.path.join(os.path.sep, BaseDir, StudyName, 'Data', 'Imaging','RawMRIData')
ExpectedRawDataZipFileLocation = os.path.join(RawDataFolder, 'tempFolderForZipFiles')

print(os.path.exists(RawDataFolder))
print(ExpectedRawDataZipFileLocation)


filename = askopenfilename(title='Select *.tar.gz file', initialdir = '~/Downloads', filetypes = [('Zipped files','*.tar.gz')])