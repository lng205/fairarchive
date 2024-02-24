import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from dotenv import load_dotenv
load_dotenv()
import os


class Post():
    cookies = {
        'user_token': os.getenv('USER_TOKEN'),
        'Hm_lvt_44d055a19f3943caa808501f424e662e': os.getenv('HM_LVT'),
        'Hm_lpvt_44d055a19f3943caa808501f424e662e': os.getenv('HM_LPVT'),
        'SERVERID': os.getenv('SERVERID'),
    }
    headers = {
        'Host': 'c.zanao.com',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'x-sc-platform': 'android',
        'x-sc-alias': 'hitsz',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309080f) XWEB/8501 Flue',
        'accept-language': '*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
    }
    @classmethod
    def get_ids(cls, from_time: str = '0'):
        headers = cls.headers
        headers['referer'] = 'https://c.zanao.com/p/home?cid=hitsz'
        params = {'from_time': from_time, 'hot': '1', 'isIOS': 'false'}
        return requests.get('https://c.zanao.com/sc-api/thread/v2/list',
                                params=params, cookies=cls.cookies, headers=headers)


    def __init__(self, thread_id: str) -> None:
        self.thread_id = thread_id
        self.headers['referer'] = f'https://c.zanao.com/p/info/{self.thread_id}?from=cate&cid=hitsz'
        self.info = self._get_info()
        try:
            self.sign = self.info.json()['data']['t_sign']
        except TypeError or requests.exceptions:
            print(f'Sign setting failed. Respose code: {self.info.status_code}. Post info: {self.info.text}')
            self.sign = None


    def _get_info(self):
        headers = self.headers
        headers['origin'] = 'https://c.zanao.com'
        # WebKitFormBoundary
        multipart_data = MultipartEncoder(
            fields={'id': self.thread_id, 'url': self.headers['referer'], 'from': 'cate', 'isIOS': 'false'})
        headers['content-type'] = multipart_data.content_type

        return requests.post('https://c.zanao.com/sc-api/thread/info', 
                                cookies=self.cookies, headers=headers, data=multipart_data)


    def get_comment(self):
        return requests.get(
            f'''https://c.zanao.com/sc-api/comment/list?id={self.thread_id}&rcid=0&vuid=0&sign={self.sign}
            &https://c.zanao.com/p/info/{self.thread_id}?from=cate&cid=hitsz&isIOS=false''',
            cookies=self.cookies, headers=self.headers)
    

if __name__ == '__main__':
    print(Post.get_ids().json())