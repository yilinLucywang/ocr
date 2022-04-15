import base64
from flask import request
from flask import Flask
import os
from flask_cors import *
import random
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="ch")

app = Flask(__name__)

CORS(app, supports_credentials=True)


@app.route("/photo", methods=['POST'])  # 不带换行的接口
def get_frame():
    # 接收图片
    upload_file = request.files['discoverPics']
    # 获取图片名
    file_name = upload_file.filename
    # 随机生成文件名称
    file_name = str(random.randint(1, 1000000)) + file_name
    file_path = r'./imgs'
    text = ""
    if upload_file:
        file_paths = os.path.join(file_path, file_name)
        upload_file.save(file_paths)
        # 调用ocr服务获得结果
        result = ocr.ocr(file_paths, cls=True)
        os.remove(file_paths)
        # 遍历获取ocr内容文本
        for line in result:
            text += line[1][0]
    text = text.replace(":", "：").replace(",", "，")
    return {"result": text}


@app.route("/photo1", methods=['POST'])  # 带换行的接口
def get_frame_1():
    # 接收图片
    upload_file = request.files['discoverPics']
    # 获取图片名
    file_name = upload_file.filename
    # 文件保存目录（桌面）
    file_name = str(random.randint(1, 1000000)) + file_name
    file_path = r'./imgs'
    text = ""
    if upload_file:
        file_paths = os.path.join(file_path, file_name)
        upload_file.save(file_paths)
        result = ocr.ocr(file_paths, cls=True)
        os.remove(file_paths)
        for line in result:
            text += line[1][0] + "\n"
    text = text.replace(":", "：").replace(",", "，")
    return {"result": text}


@app.route("/", methods=['GET'])  # 入口页面
def home():
    return """<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<title></title>
		<style>
			body,html{
				text-align: center;
			}
			#editDiv{
				width:400px;
				display: inline-block;
				height: 300px;
				background:#fff;
				border-radius:10px;
				line-height: 20px;
				padding:10px;
				font-size: 14px;
				color:#666;
				resize: none;
				outline: none;
				overflow-y: scroll;
			}
			#textAreas{
				width:400px;
				display: inline-block;
				height: 300px;
				background:#fff;
				border-radius:10px;
				line-height: 20px;
				padding:10px;
				font-size: 14px;
				color:#666;
				resize: none;
				outline: none;
				overflow-y: scroll;
			}
			#editDiv{
				border:1px solid #333;
				border-color:rgba(169,169,169,1);
				text-align: left;
			}
		</style>
	</head>
	<body>
		<div id="editDiv" contenteditable="true">
		</div>
		<textarea id="textAreas"></textarea>
	</body>
	<script src="https://ajax.aspnetcdn.com/ajax/jquery/jquery-3.5.1.min.js"></script>
	<script>
	document.querySelector('#editDiv').addEventListener('paste',function(e){
	 var cbd = e.clipboardData;
	    var ua = window.navigator.userAgent;
	    // 如果是 Safari 直接 return
	    if ( !(e.clipboardData && e.clipboardData.items) ) {
	        return ;
	    }
	    // Mac平台下Chrome49版本以下 复制Finder中的文件的Bug Hack掉
	    if(cbd.items && cbd.items.length === 2 && cbd.items[0].kind === "string" && cbd.items[1].kind === "file" &&
	        cbd.types && cbd.types.length === 2 && cbd.types[0] === "text/plain" && cbd.types[1] === "Files" &&
	        ua.match(/Macintosh/i) && Number(ua.match(/Chrome\/(\d{2})/i)[1]) < 49){
	        return;
	    }
	    for(var i = 0; i < cbd.items.length; i++) {
	        var item = cbd.items[i];
	        if(item.kind == "file"){
	            var blob = item.getAsFile();
	            if (blob.size === 0) {
	                return;
	            }
	            // blob 就是从剪切板获得的文件 可以进行上传或其他操作
	            /*-----------------------与后台进行交互 start-----------------------*/
				var data = new FormData();
				data.append('discoverPics', blob);

				$.ajax({
				    url: 'http://192.168.54.228:5000/photo',
				    type: 'POST',
				    cache: false,
				    data: data,
				    processData: false,
				    contentType: false,
				    success:function(res){
						// var obj = JSON.parse(res);
				    	console.log(res)
						$("#textAreas").val(res["result"]);
				    	$("#editDiv").empty();
				    },error:function(){

				    }
				})
				/*-----------------------与后台进行交互 end-----------------------*/
				/*-----------------------不与后台进行交互 直接预览start-----------------------*/
				// var reader = new FileReader();
				// var imgs = new Image();
				// imgs.file = blob;
				// reader.onload = (function(aImg) {
			    //   return function(e) {
			    //     aImg.src = e.target.result;
			    //   };
			    // })(imgs);
			    // reader.readAsDataURL(blob);
			    // document.querySelector('#editDiv').appendChild(imgs);
			    /*-----------------------不与后台进行交互 直接预览end-----------------------*/
	        }
	    }
	}, false);
	</script>
</html>"""


if __name__ == "__main__":
    app.run(host="0.0.0.0")  # 不指定端口的情况下为5000
