from paddleocr import PaddleOCR
import os


ocr = PaddleOCR(use_angle_cls=True, lang="ch")
img_path = '/home/install/plb/pic_result/'
files = os.listdir(img_path)
f = open("book.txt", "w", encoding="utf-8")
for i in range(len(files)):
    file = "0" * (3 - len(str(i))) + str(i) + ".png"
    file_path = img_path + file
    text = ""
    result = ocr.ocr(file_path, cls=True)
    for line in result:
        text += line[1][0]
    text = text.replace(":", "：").replace(",", "，")
    f.write(text + "\n")
