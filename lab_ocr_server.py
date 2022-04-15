import base64
from flask import request
from flask import Flask
import os
from flask_cors import *
import random
from paddleocr import PaddleOCR
import requests

ocr = PaddleOCR(use_angle_cls=True, lang="ch")

app = Flask(__name__)

CORS(app, supports_credentials=True)


@app.route("/lab", methods=['POST'])
def lab():
    title_list = ["项目名称", "检测结果", "参考区间", "单位", "试验方法"]
    upload_file = request.files['discoverPics']
    file_name = upload_file.filename
    file_name = str(random.randint(1, 1000000)) + file_name
    file_path = r'./imgs'
    text = ""
    if upload_file:
        file_paths = os.path.join(file_path, file_name)
        upload_file.save(file_paths)
        result = ocr.ocr(file_paths, cls=True)
        os.remove(file_paths)
        request_list = []
        for line in result:
            line[1] = list(line[1])
            request_list.append(str(line))
        # 调用java后处理的接口获取结果
        res = requests.post("http://192.168.54.228:8080/deepwise/getOrcStructuredResult", json=request_list)
        # 拼接展示的table对应的HTML
        for item in eval(res.content.decode()):
            temp = "<tr>"
            for title in title_list:
                if title in item:
                    temp += "<td>" + str(item[title]) + "</td>"
                else:
                    temp += "<td></td>"
            temp += "</tr>"
            text += temp
    return {"result": text}


@app.route("/", methods=['GET'])
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
				width:600px;
				display: inline-block;
				height: 600px;
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
				width:600px;
				display: inline-block;
				height: 600px;
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
		<table id="textAreas" border="1">
		    <thead>
		        <tr><th>项目名称</th><th>检测结果</th><th>参考区间</th><th>单位</th><th>试验方法</th></tr>
		    </thead>
		    <tbody></tbody>
		</table>
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
				    url: 'http://192.168.54.228:5002/lab',
				    type: 'POST',
				    cache: false,
				    data: data,
				    processData: false,
				    contentType: false,
				    success:function(res){
						// var obj = JSON.parse(res);
				    	console.log(res)
				    	$("#textAreas tbody").empty();
				    	$("#textAreas tbody").prepend(res["result"]);
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
    app.run(host="0.0.0.0", port=5002)
