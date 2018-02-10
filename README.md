# WebOCR

web在线OCR（图片文字识别）

## 效果
![](./doc/show.gif)


## features
* 在线展示结果
* 选择文件上传图片
* 粘贴板直接上传图片


## 配置
```
# 上传路径和静态文件配置路径，一般不需要改变
upload_path = os.path.join(os.path.dirname(__file__), "img")
static_path = os.path.join(os.path.dirname(__file__), "static")

# 百度OCR KEY配置，可免费申请
APP_ID = 'XXXXXXXXXX'
API_KEY = 'XXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXX'


IP = '127.0.0.1'
if(platform.system() == 'Linux'):
    IP = '0.0.0.0'
# 开放的端口，若修改，则需要修改Docker中的相关配置
PORT = 8080

```


## 使用

下载源码
```
git clone https://github.com/Sixzeroo/WebOCR
```


使用Docker容器部署（安装好Docker和Docker-compose）
```
docker-compose up -d
```

## 演示地址
http://server.liuin.cn:8080/1

## 参考
* https://github.com/layerssss/paste.js
* https://github.com/MaticsL/HFUT_cloud_print
