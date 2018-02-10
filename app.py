# -*- coding:utf-8 -*-

import os,base64,time,json

import tornado.ioloop
import tornado.web

from settings import static_path,IP,PORT

ALLOW_FILETYPE = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']

class Main1Handler(tornado.web.RequestHandler):
    def get(self):
        return self.render('web/index1.html')

class Main2Handler(tornado.web.RequestHandler):
    def get(self):
        return self.render('web/index2.html')


class UploadFile2Handler(tornado.web.RequestHandler):

    def post(self):
        from settings import upload_path
        from ocr import OCR

        now_time = time.strftime('%Y-%m-%dT%H-%M-%S',time.localtime(time.time()))
        dir_prefix = now_time

        try:
            file_metas = self.request.files['file']
        except:
            return self.render('web/result.html', result='negative', result_header='失败', result_content='请选择需要打印的文件。')

        for meta in file_metas:
            filename = meta['filename']
            # valid filetype
            if not os.path.splitext(filename)[1] in ALLOW_FILETYPE:
                return self.render('web/result.html', result='negative', result_header='上传失败',
                                       result_content='文件格式不支持')

            try:
                os.makedirs(os.path.join(upload_path, dir_prefix))
            except:
                pass
            # save file
            filepath = os.path.join(upload_path, dir_prefix, "img"+os.path.splitext(filename)[1])
            with open(filepath,'wb') as up:
                up.write(meta['body'])
            # orc
            ocrinstance = OCR()
            res = ocrinstance.getResult(filepath)
            statusCode = res['code']
            status = '成功' if (statusCode == 1) else '失败'
            text = res['text']
            # save res
            respath = os.path.join(upload_path, dir_prefix, 'result.txt')
            with open(respath, 'w',encoding="utf-8") as info:
                info.write(status+'\n'+text)
            # render
            if(statusCode == 1):
                return self.render('web/result.html', result='positive', result_header=status, result_content=text)
            else:
                return self.render('web/result.html', result='negative', result_header=status, result_content=text)


class UploadFile1Handler(tornado.web.RequestHandler):

    def post(self):
        from settings import upload_path
        from ocr import OCR

        now_time = time.strftime('%Y-%m-%dT%H-%M-%S', time.localtime(time.time()))
        dir_prefix = now_time

        try:
            base64ImgData = self.request.arguments['data'][0].decode("utf-8")
            # 去除base64图片前面的说明str
            base64ImgData = base64ImgData[base64ImgData.find(',') + 1:]
            imgData = base64.b64decode(base64ImgData)
        except:
            self.finish({
                'code': 0,
                'message': "error"
            })

        try:
            os.makedirs(os.path.join(upload_path, dir_prefix))
        except:
            pass

        # save file
        filepath = os.path.join(upload_path, dir_prefix, "img.png" )
        with open(filepath, 'wb') as up:
            up.write(imgData)
        # orc
        ocrinstance = OCR()
        res = ocrinstance.getResult(filepath)
        statusCode = res['code']
        status = '成功' if (statusCode == 1) else '失败'
        text = res['text']
        # save res
        respath = os.path.join(upload_path, dir_prefix, 'result.txt')
        with open(respath, 'w', encoding="utf-8") as info:
            info.write(status + '\n' + text)

        self.finish({
            'code': statusCode,
            'message': text
        })


application = tornado.web.Application([
    (r"/", tornado.web.RedirectHandler,{"url":"/1","permanent":False}),
    (r"/1", Main1Handler),
    (r"/2", Main2Handler),
    (r"/1/upload", UploadFile1Handler),
    (r"/2/upload", UploadFile2Handler)],
    static_path=static_path)

if __name__ == "__main__":
    application.listen(PORT, address=IP)
    tornado.ioloop.IOLoop.instance().start()
