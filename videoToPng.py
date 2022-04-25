import PIL
from PIL import Image
from itertools import product
import os
import sys

def tile(filenames, dir_in, dir_out):
    for i in range(len(filenames)):
        filename = filenames[i]
        name, ext = os.path.splitext(filename)
        img = Image.open(os.path.join(dir_in, filename))
        w, h = img.size
        #cut the upper part of every pic
        preprocessPath = os.path.join(dir_in, filename)
        initBox = (0, 403, w, h)
        img.crop(initBox).save(preprocessPath)
        #loop through the entire y value and find the color changing part of the graph and store that in a graph
        preprocessedImage = PIL.Image.open(preprocessPath)
        w, h = preprocessedImage.size
        boundaries = [0]
        prevColor = 240
        for k in range(h): 
            color = preprocessedImage.getpixel((w - 61, k))
            #exclude black
            avgColor = (1/3) * (color[0] + color[1] + color[2])
            if(abs(avgColor - prevColor) > 40): 
                boundaries.append(k)
            prevColor = avgColor
        #cut at those color changing part 
        for j in range(len(boundaries) - 1):
            nameNumber = str(j)
            if(j//10 < 1): 
                nameNumber = "0" + str(j)
            box = (0, boundaries[j], w, boundaries[j + 1])
            out = os.path.join(dir_out, f'{name}_{nameNumber}{ext}')
            preprocessedImage.crop(box).save(out)

def main():
    img_names = []
    path_str = sys.argv[1]
    img_names = path_str.split(" ")
    file_in_path = img_names[0]
    file_out_path = img_names[1]
    tile(img_names[2:], file_in_path, file_out_path)
main()

#local test
# def main(): 
#     filenames = ['WechatIMG10.png','WechatIMG13.png' ]
#     tile(filenames, '/Users/wangyilin/Desktop/uploadFolder', '/Users/wangyilin/Desktop/exampleOut')
# main()
