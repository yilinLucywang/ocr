#!/bin/bash
#cut images
rm -R /Users/wangyilin/Desktop/imagesPic
mkdir /Users/wangyilin/Desktop/imagesPic
input_path="/Users/wangyilin/Desktop/uploadFolder"
output_path+='/Users/wangyilin/Desktop/imagesPic'
for entry in `ls $input_path`; do
        cur_output_path="$output_path"
        cur_output_path+="/"
        cur_output_path+="$entry"
        mkdir "$cur_output_path"
        param_var="$input_path"
        param_var+=" "
        param_var+="$cur_output_path"
        param_var+=" "
        param_var+="$entry"
        python3 /Users/wangyilin/Desktop/videoToPng.py "$param_var"
done

#do OCR
img_path='/Users/wangyilin/Desktop/imagesPic'
full_path=""
for entry in `ls -v $img_path`; do
        cur_path="$img_path"
        cur_path+="/"
        cur_path+="$entry"
        input_path=""
        for image in `ls -v $cur_path`; do
        	input_path+="$cur_path"
        	input_path+="/"
        	input_path+="$image "
        done
        python3 /Users/wangyilin/Downloads/ocr/fast_demo.py "$input_path"
done

#make tree
txt_paths=""
folder_path="/Users/wangyilin/Desktop/imagesPic"
for entry in `ls -v $folder_path`; do
	txt_path="$folder_path"
	txt_path+="/"
    txt_path+="$entry"
    txt_path+="/"
    txt_path+="ocrResult.txt"
    txt_paths+="$txt_path"
    txt_paths+=" "
done
	python3 /Users/wangyilin/Desktop/processConversationTree.py "$txt_paths"





