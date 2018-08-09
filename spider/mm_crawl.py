import time
import lxml
import random
import requests
from lxml import etree


class Spider(object):
    """爬取妹子图首页图片"""
    def __init__(self):
        self.data_list = []
        self.url = 'http://www.mmjpg.com'
        self.headers = {
            # 响应报文前不能留有空格
            'Accept'                   :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language'          :'zh-CN,zh;q=0.9',
            'Host'                     :'www.mmjpg.com',
            'Proxy-Connection'         :'keep-alive',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent'               :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Referer'                  :'http://www.mmjpg.com'
        }

    def send_requests(self):
        """向目标网页发送请求"""
        res = requests.get(self.url, headers=self.headers).content
        return res

    def get_pic_urls(self, res):
        """获取图片链接"""
        html_data = etree.HTML(res)
        pic_urls = html_data.xpath('//div[@class="pic"]/ul/li/a/img/@src')
        pic_names = html_data.xpath('//div[@class="pic"]/ul/li/a/img/@alt')

        for i in range(len(pic_urls)):
            pic_datas = dict(pic_name=pic_names[i], pic_url=pic_urls[i])
            self.data_list.append(pic_datas)
        print(self.data_list)


    def main(self):
        res = self.send_requests()
        self.get_pic_urls(res)
        pics = self.data_list
        for i in range(len(pics)):
            res_pics = requests.get(pics[i]['pic_url'], headers=self.headers)
            pic_name = pics[i]['pic_name']
            time.sleep(random.randint(0, 2))
            keys = (str(i + 1), '-', pic_name, '.png')
            pic_name =  ''.join(keys)
            print("正在爬取:%s" % pic_name)
            with open(pic_name, 'wb')as f:
                f.write(res_pics.content)


if __name__ == '__main__':
    spider = Spider()
    spider.main()