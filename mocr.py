import os
import numpy as np
from network import Network

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
    for x in range(img.width):
        for y in range(img.height):
            pdata.append(pixels[x,y])
    cells.append((np.array(pdata), int(number)))

net = Network([150,30,10])
net.SGD(cells,100,1,3,cells)
