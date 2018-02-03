# -*- coding:utf-8 -*-

import os
import time
import tornado.ioloop
import tornado.web

from settings import static_path,IP,PORT

ALLOW_FILETYPE = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render('web/index.html')


class UploadFileHandler(tornado.web.RequestHandler):

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
            with open(respath, 'w') as info:
                info.write(status+'\n'+text)
            # render
            if(statusCode == 1):
                return self.render('web/result.html', result='positive', result_header=status, result_content=text)
            else:
                return self.render('web/result.html', result='negative', result_header=status, result_content=text)


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload", UploadFileHandler)],
    static_path=static_path)

if __name__ == "__main__":
    application.listen(PORT, address=IP)
    tornado.ioloop.IOLoop.instance().start()
