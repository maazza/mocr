import os
import pickle
import numpy as np
import time
from network2 import MLP

from PIL import Image

BLACK = 0
WHITE = 255

cdir = "cells"
cells = []

for cell in os.listdir(cdir):
    img = Image.open(os.path.join(cdir,cell))
    number = cell.split(".")[0][-1]
    pixels = img.load()
    pdata = []
    target = [0]*10
    for x in range(img.width):
        for y in range(img.height):
            pdata.append(1 if pixels[x,y] == WHITE else 0)
    target[int(number)] = 1
    cells.append((np.array(pdata), target))

stime = time.time()
    
net = None
if os.path.exists('net.pkl'):
    print("loaded")
    net_file = open('net2.pkl','rb')
    net = pickle.load(net_file)
    net_file.close()
else:
    net = MLP(150,30,10)
    net.train(cells,500,2)
print("dumped")
net_file = open("net2.pkl",'wb')
pickle.dump(net,net_file)
net_file.close()
    
etime = time.time() -stime
print("%s min %s secs" % (int(etime/60),etime%60))
for cell in cells:
    res = np.argmax(net.predict(cell[0]))
    correct = np.argmax(cell[1])
    if res != correct:
        print("found %s instead of %s" % (res, correct))
