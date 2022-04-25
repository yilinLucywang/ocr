import sys
import PIL
from paddleocr import PaddleOCR, draw_ocr
import unicodedata
import io
from PIL import Image
import wordninja

def roughCorrect(text): 
        for k in range(len(text) - 3): 
                frame = text[k:k+4]
                if(frame == " ive"):
                        text = text[0:k] + ' I\'ve'+ text[k+4:]
                if(frame == " ld "):
                        print(text)
                        text = text[0:k] + ' I\'d ' + text[k+4:]
                        print(text)

        for i in range(len(text) - 2):
                frame = text[i:i+3]
                if(frame == "l '"):
                        text = text[0:i] + 'I\''+ text[i+3:]
                if(frame == " l "):
                        text = text[0:i] + ' I '+ text[i+3:]

        for j in range(len(text) - 1): 
                shorterText = text[j:j+2]
                if(shorterText == "l'"):
                        text = text[0:j] + 'I\'' + text[j+2:]
                if(shorterText == "lf"): 
                        text = text[0:j] + 'If' + text[j+2:]
                if(shorterText == "lt"): 
                        text = text[0:j] + 'It' + text[j+2:]
                if(shorterText == "dn"):
                        text = text[0:j] + 'on' + text[j+2:]
        return text

def runOCR(img_paths, out_path):
        ocr = PaddleOCR(use_angle_cls=True, lang="ch") # need to run only once to download and load model into memory
        with open(out_path+"/"+"ocrResult.txt", "w") as f:
                for i in range(len(img_paths)):
                        # print(i)
                        img_path = img_paths[i]
                        # print(img_path)

                        #open image
                        image = PIL.Image.open(img_path)
                        w, h = image.size
                        if(h < 50): 
                                continue
                        result = ocr.ocr(img_path, cls=True)
                        #0 stands for left; 1 stands for right; assumes always starting from left
                        prev = 1
                        prevIsUser = True
                        for line in result:
                                upperLeft = line[0][0]
                                lowerRight = line[0][2]
                                leftDist = upperLeft[0]
                                halfHeight = h//2
                                samplePoint = (w - 61, halfHeight)
                                curColor = image.getpixel((samplePoint[0], samplePoint[1]))
                                avg = (curColor[0] + curColor[1] + curColor[2])/3
                                isUser = False
                                text = str(line[1][0])
                                text = " ".join(wordninja.split(text))
                                text = roughCorrect(text)
                                # print(text)
                                if(avg < 200):
                                        isUser = True
                                if isUser:
                                        f.write( "\n" + "user: " + text + " ")
                                else:
                                        if(prevIsUser != isUser): 
                                                f.write("\n" + "bot: " + text + " ")
                                        else: 
                                                f.write(text + " ")
                                prevIsUser = isUser
def main():
        img_paths = []
        path_str = sys.argv[1]
        img_paths = path_str.split(" ")
        img_paths.pop()
        sys.argv = [sys.argv[0]]
        img_paths.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
        parts = img_paths[0].split("/")
        out_path = ''
        for i in range(len(parts) - 1): 
                out_path+=parts[i]
                out_path+="/"
        out_path = out_path[:len(out_path) - 1]
        runOCR(img_paths, out_path)
main()

#TODO: This is for local test
# def main():
#         img_paths = ['/Users/wangyilin/Desktop/imagesPic/WechatIMG14_09.png']
#         runOCR(img_paths)
# main()