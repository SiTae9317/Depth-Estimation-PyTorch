import os
import shutil
import pickle
import random

from GeneratePPMPGM import genPPMPGM

imageType = ".png"

baseDrive = "f://"
baseFolder = "NIA대용량"

dataDrive = "d://"
dataFolder = "Projects/Pytorch/Depth-Estimation/NiaDataset"

datasetDict = {}

datasetDir = "NiaDataset"

gppm = genPPMPGM()

for dir1 in os.listdir("{}{}".format(baseDrive, baseFolder)):
    rgbPath = ""
    depthPath = ""
    for dir2 in os.listdir("{}{}/{}".format(baseDrive, baseFolder,dir1)):
        curDir = dir2.split('.')[2].lower()
        
        if curDir == 'images':
            rgbPath = baseDrive + baseFolder + '/' + dir1 + '/' + dir2
        elif curDir == 'depth':
            depthPath = baseDrive + baseFolder + '/' + dir1 + '/' + dir2
            
    for file in os.listdir(rgbPath):
        fileSplit = file.split('.')
        if fileSplit[1].lower() == "png" :
            fileName = fileSplit[0]
            try :  
                if gppm.setData(fileName + imageType, rgbPath, dataDrive + dataFolder+"/train_rgb", 'P6') :
                    if gppm.setData(fileName + "_DEPTH" + imageType, depthPath, dataDrive + dataFolder+"/train_depth", 'P5') :
                        print(fileName+".ppm :" + fileName + "_DEPTH.pgm")
                        datasetDict[fileName+".ppm"] = fileName + "_DEPTH.pgm"
            except :
                pass
        
fpkl = open("./{}/index.pkl".format(datasetDir),'wb')
pickle.dump(datasetDict,fpkl)
fpkl.close()
        
train_dict = pickle.load(open("./{}/index.pkl".format(datasetDir),'rb'))
test_dict = {}
train_r_list = list(train_dict.keys())
print(len(train_r_list))
test_r_list = random.sample(train_r_list,int(len(train_r_list)/4))

for r_file in test_r_list:
    d_file = train_dict[r_file]
    shutil.move("./{}/train_rgb/{}".format(datasetDir, r_file),"./{}/test_rgb/{}".format(datasetDir, r_file))
    shutil.move("./{}/train_depth/{}".format(datasetDir, d_file),"./{}/test_depth/{}".format(datasetDir, d_file))
    test_dict[r_file] = d_file
    train_dict.pop(r_file)
    
test_pkl = open("./{}/index2.pkl".format(datasetDir),'wb')
train_pkl = open("./{}/index1.pkl".format(datasetDir),'wb')
pickle.dump(train_dict,train_pkl)
pickle.dump(test_dict,test_pkl)

test_pkl.close()
train_pkl.close()