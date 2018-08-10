import os
import re
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
        self.folder_path = './mmjpg'

    def get_total_num(self):
        """向目标网页发送请求"""
        res = requests.get(self.url, headers=self.headers).content
        html_data = etree.HTML(res)
        pages = html_data.xpath("//div[@class='page']/em[@class='info']/text()")[0]
        page_num = re.search(r'.*?(\d+).*', pages).group(1)
        return page_num

    def create_folder(self, title):
        if not os.path.isdir(self.folder_path):
            os.mkdir(self.folder_path)
        self.folder_path = os.path.join(self.folder_path, title)
        print(self.folder_path)
        try:
            os.mkdir(self.folder_path)
        except:
            pass
        os.chdir(self.folder_path)

    def send_request_to_url(self, num):
        """向用户指定页码发送请求"""
        if num > int(self.get_total_num()):
            print("您请求的页码%d不存在!!!" % num)
            return 'error'
        elif num == 1:
            url = self.url
        else:
            url = self.url + '/home/%d' % num
        res = requests.get(url, headers=self.headers).content
        return res

    def get_titles(self, res):
        """获取指定页码对应图片标题以及图片链接列表"""
        html_data = etree.HTML(res)
        titles_list = html_data.xpath("//span[@class='title']/a/text()")
        # 获取套图的详细位置
        pics_urls = html_data.xpath("//span[@class='title']/a/@href")
        # self.pics_urls = pics_urls
        for i in range(len(titles_list)):
            titles_list[i] = '%s. ' % (i+1) + titles_list[i]
        titles = '\n'.join(titles_list)
        print(titles)
        pic_num = int(input("请输入图片编号:"))
        pic_info = [titles_list[pic_num - 1], pic_num, pics_urls[pic_num - 1]]
        print(pic_info)
        return pic_info


    def send_to_pics_urls(self, pic_info):
        """获取图片对应的url"""
        print(pic_info[0], pic_info[2])
        self.title = pic_info[0]
        ret = requests.get(pic_info[2], headers=self.headers).content
        html_data = etree.HTML(ret)
        res = html_data.xpath("//div[@class='page']/a[last()-1]/text()")[0]
        pic_urls_list = [pic_info[2] + '/%s' % str(i) for i in range(1, int(res)+1) if i != 1]
        pic_urls_list.insert(0, pic_info[2])
        print(pic_urls_list)
        return pic_urls_list


    def get_mm_pics(self, pic_urls_list):
        """获取图片链接列表"""
        for i in range(len(pic_urls_list)):
            time.sleep(random.randint(0, 2))
            ret = requests.get(pic_urls_list[i], headers=self.headers).content
            html_data = etree.HTML(ret)
            pics = html_data.xpath('//div[@class="content"]/a/img/@src')[0]
            self.data_list.append(pics)


    def main(self):
        total_page_num = self.get_total_num()
        print("总页码数为:%d" % int(total_page_num))
        page = int(input("请输入您选择的页码数:"))
        res = self.send_request_to_url(page)
        if res == 'error':
            return

        pic_info = self.get_titles(res)
        pic_urls_list = spider.send_to_pics_urls(pic_info)
        self.get_mm_pics(pic_urls_list)
        self.demo_name = re.match(r'.*?\s(.*)', self.title).group(1)
        self.create_folder(self.demo_name)

        list_pics = self.data_list
        for i in range(len(list_pics)):
            res_pics = requests.get(list_pics[i], headers=self.headers)
            time.sleep(random.randint(0, 2))
            keys = (self.title, '_%s' % str(i+1), '.png')
            pic_name =  ''.join(keys)
            print("正在爬取:%s" % pic_name)
            with open(pic_name, 'wb')as f:
                f.write(res_pics.content)


if __name__ == '__main__':
    spider = Spider()
    spider.main()