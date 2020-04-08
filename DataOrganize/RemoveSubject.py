# Remove a subject
import os
import sys
import glob
import shutil
import datetime


if len(sys.argv) < 1:
    print('Usage: RemoveSubject.py <SubjectID (eg #)>')
    sys.exit(0)
else:
    Subid = "%d"%(int(sys.argv[1]))

BaseDir = os.path.join("/media","jsteffen","Data001","NeuralCognitiveMapping","Imaging")
shutil.rmtree(os.path.join(BaseDir,'RawMRIData',Subid))
shutil.rmtree(os.path.join(BaseDir,'BehavioralData',Subid))
shutil.rmtree(os.path.join(BaseDir,'ProcMRIData',Subid))

