from paddleocr import PaddleOCR
import os

ocr = PaddleOCR(use_angle_cls=True, lang="ch") # need to run only once to download and load model into memory
img_path = 'imgs/'
files = os.listdir(img_path)
result_path = "result/"
for file in files:
    result = ocr.ocr(img_path+file, cls=True)
    f = open(result_path+file+".txt","w",encoding="utf-8")
    for line in result:
        f.write(line[1][0]+"\n")
    f.close()

