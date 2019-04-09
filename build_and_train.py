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

NET_PATH = "net.pkl"
net = None
if os.path.exists(NET_PATH):
    print("loaded")
    with open(NET_PATH,'rb') as net_file:
        net = pickle.load(net_file)
else:
    net = MLP(150,30,10)
    net.train(cells,500,2)
    with open(NET_PATH,'rb') as net_file:
        pickle.dump(net,net_file)
    print("dumped")
    
etime = time.time() -stime
print("%s min %s secs" % (int(etime/60),etime%60))
for cell in cells:
    res = np.argmax(net.predict(cell[0]))
    correct = np.argmax(cell[1])
    if res != correct:
        print("found %s instead of %s" % (res, correct))
