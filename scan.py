import os
from PIL import Image

BLACK = 0
WHITE = 255

original = "sudo2.png"
Img = Image.open(original)
gray = Img.convert('L')
bw = gray.point(lambda x: BLACK if x<200 else WHITE, '1')
result = "sudo2_bw.png"
result_dir = os.path.dirname(result)
print(result_dir)
bw.save(result)

pixels = bw.load()
fheight = 0 #height off the first cell
fwidth = 0
lheight = 0 #height off the last cell
lwidth = 0

try:
    for x in range(bw.width):
        for y in range(bw.height):
            if pixels[x,y] != BLACK:
                fheight = y
                fwidth = x
                raise StopIteration
except StopIteration:
    pass

try:
    for x in range(bw.width):
        for y in range(bw.height):
            if pixels[bw.width - x -1,bw.height - y -1] != BLACK:
                lheight = bw.height - y -1
                lwidth = bw.width - x -1
                raise StopIteration
except StopIteration:
    pass

print(fwidth,fheight)
print(lwidth,lheight)

crop = bw.crop((fwidth,fheight,lwidth,lheight))
crop.save(result)
pixels = crop.load()
cells = []

def empty_cell(x,y,width,height):
    count = 0
    for i in range(width):
        for j in range(height):
            if pixels[x+i ,y+j] == BLACK:
                count +=1
                if count > 3:
                    return False
    return True

def crop_number(x,y,width,height):
    left = 0
    right = width
    top=0
    bottom = height
    try:
        for i in range(width):
            for j in range(height):
                if pixels[x+i ,y+j] == BLACK:
                    left = i
                    raise StopIteration
    except StopIteration:
        pass
    try:
        for i in range(width):
            for j in range(height):
                if pixels[x+width-i-1 ,y+j] == BLACK:
                    right = width - i
                    raise StopIteration
    except StopIteration:
        pass
    try:
        for j in range(height):
            for i in range(width):
                if pixels[x+i ,y+j] == BLACK:
                    top = j
                    raise StopIteration
    except StopIteration:
        pass
    try:
        for j in range(height):
            for i in range(width):
                if pixels[x+i ,y+height-j-1] == BLACK:
                    bottom =height-j
                    raise StopIteration
    except StopIteration:
        pass
    return crop.crop((x+left,y+top,x+right,y+bottom))
    
    
x= 0
y= 0
while x < crop.width:
    y=0
    cwidth =0
    while y < crop.height and x < crop.width:
        if pixels[x,y] == WHITE:
            cwidth = 0
            cheight = 0
            for i  in range(crop.width-x):
                if pixels[x+i,y] == BLACK:
                   cwidth = i
                   break
            for j in range(crop.height-y):
                if pixels[x,y+j] == BLACK:
                   cheight = j
                   break
            if cwidth == 0:
                cwidth = crop.width -x
            if cheight == 0:
                cheight = crop.height - y
            if not empty_cell(x,y,cwidth,cheight):
                cells.append(crop_number(x,y,cwidth,cheight))
            y+= cheight
        y+=1
    x+= cwidth
    x+=1

print(len(cells))
nb=0
for cell in cells:
    print(cell.height, cell.width)
    ck = cell.resize((10,15))
    ck.save(os.path.join(result_dir,"cells","cell_%s.png" % nb))
    nb+=1
            
    
