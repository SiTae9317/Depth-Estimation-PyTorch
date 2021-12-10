import cv2
import numpy as np
from PIL import Image
import struct

class genPPMPGM :            
    def setData(self, name, path, savePath, ftype) :
        cName = name.split('.')[0]
        cType = ftype
        cSavePath = savePath
        
        try:
            img_array = np.fromfile(path + '/' + name, np.uint8)
            src = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            npImage = np.array(src)
            npImage = npImage[:, 160:1120]
            npImage = cv2.resize(npImage, dsize=(640, 480), interpolation=cv2.INTER_AREA)
            npImage = npImage.reshape(640 * 480, 3)

            if cType == 'P5':
                return self.generateP5(cName, cSavePath, cType, npImage)
            elif cType == 'P6':
                return self.generateP6(cName, cSavePath, cType, npImage)
        except:
            print(name + " excpet")
            return False
        
    def generateP5(self, name, savePath, ftype, npImage):
        try:
            print("{}/{}.pgm".format(savePath, name))
            pgmfile=open("{}/{}.pgm".format(savePath, name),'wb+') # note the binary flag
            pgmfile.write(("%s\n" % (ftype)).encode('utf-8')) 
            pgmfile.write(("%d %d\n" % (640, 480)).encode('utf-8')) 
            pgmfile.write(("65535\n").encode('utf-8'))
            npImage = npImage[:, :1]
            npImage = np.array(npImage, dtype=np.uint16)

            for curVal in npImage:
                pgmfile.write(struct.pack( "<H", curVal[0] ))
            pgmfile.close()
            return True
        except:
            print(name + "p5 except")
            return False
            
    def generateP6(self, name, savePath, ftype, npImage):
        try:
            print("{}/{}.ppm".format(savePath, name))
            ppmfile=open("{}/{}.ppm".format(savePath, name),'wb+') # note the binary flag
            ppmfile.write(("%s\n" % (ftype)).encode('utf-8')) 
            ppmfile.write(("%d %d\n" % (640, 480)).encode('utf-8')) 
            ppmfile.write(("255\n").encode('utf-8'))

            for red,green,blue in npImage:
                ppmfile.write(blue.tobytes('c'))
                ppmfile.write(green.tobytes('c'))
                ppmfile.write(red.tobytes('c'))
            ppmfile.close()
            return True
        except:
            print(name + "p6 except")
            return False