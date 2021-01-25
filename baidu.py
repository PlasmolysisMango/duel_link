import requests
import base64
from io import BytesIO

APP_KEY = 'rXGQpX6DIavNqVoVMZ7r3804'
SECRET_KEY = 'yWwxn889WFjaR2P14AM1HVn60a4jGPMD'
# 修改为自己申请的百度api

class BaiduOCR(object):
    def __init__(self, AKey, SKey):
        self.app_key = AKey
        self.secret_key = SKey
    
    def get_access_token(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(self.app_key, self.secret_key)
        response = requests.get(host)
        if response:
            resjson = response.json()
            if resjson['access_token']:
                return resjson['access_token']
            else:
                print('access_token error!')
    
    def read(self, img, lang = 'CHN_ENG'):
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG')
        byte_data = output_buffer.getvalue()
        img_b64 = base64.b64encode(byte_data)
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
        data = {"image": img_b64, 'language_type': 'CHN_ENG'}
        access_token = self.get_access_token()
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data = data, headers = headers)
        if response:
            resjson = response.json()
            if resjson['words_result']:
                word = resjson['words_result'][0]['words'].replace(' ', '')
                return word