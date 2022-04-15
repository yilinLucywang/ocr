#!/bin/bash
img_path='/Users/wangyilin/Downloads/ocr/importedImages'
full_path=""
for entry in `ls $img_path`; do
	cur_path=""
	cur_path+="$img_path"
	cur_path+='/'
	cur_path+="$entry"
	full_path+="$cur_path"
	full_path+=' '
done
python3 /Users/wangyilin/Downloads/ocr/fast_demo.py "$full_path"