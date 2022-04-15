from paddleocr import PaddleOCR, draw_ocr
import os
from PIL import Image
import tqdm

# Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
# 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

file_list = os.listdir("检验单")
for file in tqdm.tqdm(file_list):
    img_path = "检验单/" + file
    txt_path = "txt/" + file + ".txt"
    res_path = "res/" + file + ".jpg"
    result = ocr.ocr(img_path, cls=True)
    f = open(txt_path, "w")
    for line in result:
        f.write(str(line) + "\n")
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='lib/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save(res_path)