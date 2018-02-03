from aip import AipOcr

from settings import API_KEY,APP_ID,SECRET_KEY

class OCR(object):
    def __init__(self):
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    @staticmethod
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            content = fp.read()
            fp.close()
            return content

    def getResult(self,filePath):
        '''
        返回OCR识别结果
        :param filePath: 图片路径
        :return: {'code': 0/1 （是否成功）,'text':str （信息）}
        '''
        image = OCR.get_file_content(filePath)

        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"

        res = self.client.basicGeneral(image,options)
        output = {'code': 0,
                  'text': ''}
        # 出错情况
        if( 'error_code' in res):
            output['code'] = 0
            if(res['error_code'] == '17'):
                output['text'] = "每天流量超限额"
            else:
                output['text'] = '错误代码：{}'.format(res['error_code'])
        # 正常情况
        else:
            output['code'] = 1
            text = ''
            for elem in res['words_result']:
                text = text + elem['words']
            output['text'] = text

        return output


# if __name__ == '__main__':
#     test = OCR()
#     a = test.getResult('H:\\pro\\WebOCR\\img\\2018-02-02T22-42-08.PNG')
#     print(a)