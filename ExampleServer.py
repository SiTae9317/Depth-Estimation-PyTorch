import numpy as np
import os
import time
import torch
import cv2
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
import torch.utils.data as data
from PIL import Image
from torchvision.transforms import Resize, Compose, ToPILImage, ToTensor
import math
import matplotlib.pyplot as plt
from torchvision.models.resnet import resnet101
import argparse
from SocketWebServer.DeviceWebServer import DeviceWebServer

def smooth(in_planes, out_planes):
    return nn.Sequential(
        nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=1, padding=1),
        nn.ReLU(),
    )

def predict(in_planes, out_planes):
    return nn.Sequential(
        nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=1, padding=1),
        nn.ReLU(),
    )

class I2D(nn.Module):
    def __init__(self, pretrained=True):
        super(I2D, self).__init__()

        resnet = resnet101(pretrained=pretrained)

        self.layer0 = nn.Sequential(resnet.conv1, resnet.bn1, resnet.relu, resnet.maxpool)
        self.layer1 = nn.Sequential(resnet.layer1) # 256
        self.layer2 = nn.Sequential(resnet.layer2) # 512
        self.layer3 = nn.Sequential(resnet.layer3) # 1024
        self.layer4 = nn.Sequential(resnet.layer4) # 2048

        # Top layer
        self.toplayer = nn.Conv2d(2048, 256, kernel_size=1, stride=1, padding=0)  # Reduce channels

        # Lateral layers
        self.latlayer1 = nn.Conv2d(1024, 256, kernel_size=1, stride=1, padding=0)
        self.latlayer2 = nn.Conv2d( 512, 256, kernel_size=1, stride=1, padding=0)
        self.latlayer3 = nn.Conv2d( 256, 256, kernel_size=1, stride=1, padding=0)

        # Smooth layers
        self.smooth1 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)
        self.smooth2 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)
        self.smooth3 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)
        
        # Depth prediction
        self.predict1 = smooth(256, 64)
        self.predict2 = predict(64, 1)
        
    def _upsample_add(self, x, y):
        '''Upsample and add two feature maps.
        Args:
          x: (Variable) top feature map to be upsampled.
          y: (Variable) lateral feature map.
        Returns:
          (Variable) added feature map.
        Note in PyTorch, when input size is odd, the upsampled feature map
        with `F.upsample(..., scale_factor=2, mode='nearest')`
        maybe not equal to the lateral feature map size.
        e.g.
        original input size: [N,_,15,15] ->
        conv2d feature map size: [N,_,8,8] ->
        upsampled feature map size: [N,_,16,16]
        So we choose bilinear upsample which supports arbitrary output sizes.
        '''
        _,_,H,W = y.size()
        return F.interpolate(x, size=(H,W), mode='bilinear', align_corners=False) + y

    def forward(self, x):
        _,_,H,W = x.size() # batchsize N,channel,height,width
        
        # Bottom-up
        c1 = self.layer0(x) 
        c2 = self.layer1(c1) # 256 channels, 1/4 size
        c3 = self.layer2(c2) # 512 channels, 1/8 size
        c4 = self.layer3(c3) # 1024 channels, 1/16 size
        c5 = self.layer4(c4) # 2048 channels, 1/32 size

        # Top-down
        p5 = self.toplayer(c5)
        p4 = self._upsample_add(p5, self.latlayer1(c4)) # 256 channels, 1/16 size
        p4 = self.smooth1(p4) 
        p3 = self._upsample_add(p4, self.latlayer2(c3)) # 256 channels, 1/8 size
        p3 = self.smooth2(p3) # 256 channels, 1/8 size
        p2 = self._upsample_add(p3, self.latlayer3(c2)) # 256, 1/4 size
        p2 = self.smooth3(p2) # 256 channels, 1/4 size

        return self.predict2( self.predict1(p2) )     # depth; 1/4 size, mode = "L"
    
def modelProcess(image_bytes):
    #print('runtest')
    rgb = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    
    data = Compose([ToTensor()])(rgb).float()
    data = data.unsqueeze(0)
    data = data.to(DEVICE)
            
    pred_depth = i2d(data)
    depth_img = transforms.ToPILImage()(pred_depth.int().squeeze(0))
    return depth_img.tobytes()

def initializeModel():
    # dataset
    LOAD_DIR = '.'
    print(torch.cuda.get_device_name(0))
    print(torch.cuda.is_available())
    print(torch.__version__)
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #eval_dataset = NYUv2Dataset()
    #eval_dataloader = torch.utils.data.DataLoader(eval_dataset, batch_size=1,shuffle=True)
    i2d = I2D().to(DEVICE)
    i2d.load_state_dict(torch.load('{}/fyn_model.pt'.format(LOAD_DIR),map_location='cuda'))
    print("model loaded")
    # setting to eval mode
    i2d.eval()
    print('evaluating...')
    return i2d, DEVICE
    
if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description="-p set port number\n") 
    parser.add_argument('-p', help="port", required=True) 
    args = parser.parse_args() 
    
    try: 
        port = int(args.p) 
        
        i2d, DEVICE = initializeModel()
    
        server = DeviceWebServer('', port)
        server.addHandler('/SingleDepthEstimation', modelProcess)
        server.runServer()
    except: 
        print("Port Error")
        pass 
    