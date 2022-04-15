import sys
import PIL
from paddleocr import PaddleOCR, draw_ocr
def runOCR(img_paths):
	ocr = PaddleOCR(use_angle_cls=True, lang="ch") # need to run only once to download and load model into memory
	f = open("ocrResult.txt", "w")
	f.close()
	for i in range(len(img_paths)): 
		img_path = img_paths[i]
		image = PIL.Image.open(img_path)
		w, h = image.size
		result = ocr.ocr(img_path, cls=True)
		classifier = []
		for line in result:
			print(line)
			upperLeft = line[0][0]
			lowerRight = line[0][2]
			leftDist = upperLeft[0]
			if(lowerRight[0] > (w - leftDist)):
				classifier.append("user")
				f = open("ocrResult.txt", "a")
				f.write("user: " + str(line[1][0]) + "\n")
			else: 
				classifier.append("bot")
				f = open("ocrResult.txt", "a")
				f.write("bot: " + str(line[1][0]) + "\n")
		f.close()

def main(): 
	img_paths = []
	path_str = sys.argv[1]
	img_paths = path_str.split(" ")
	img_paths.pop()
	sys.argv = [sys.argv[0]]
	runOCR(img_paths)
main()