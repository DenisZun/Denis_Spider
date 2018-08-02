import re
import time
import random
import requests
from requests import RequestException


class Spider(object):
    """猫眼电影排行榜前100爬虫"""
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
            "Mozilla/5.0 (Macintosh;U;IntelMacOSX10_6_8;en-us) AppleWebKit/534.50(KHTML,likeGecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows;U;WindowsNT6.1;en-us) AppleWebKit/534.50 (KHTML,likeGecko) Version/5.1 Safari/534.50"
        ]
        self.headers = {
            "User-Agent": random.choice(self.user_agents)
        }
        self.num = 0
        self.url = "http://maoyan.com/board/4"

    def get_hot_page(self, url):
        ret = None
        try:
            res = requests.get(url, headers=self.headers)
            if res.status_code == 200:
                response = res.text
                ret = self.parse_page(response)
                return ret
        except RequestException:
            return ret

    def parse_page(self, response):
        film_no_pattern = re.compile(r'<dd>.*?board-index.*?>(.*?)</i>', re.S)
        film_info_pattern = re.compile(r'<dd>.*?<img.*?data-src="(.*?)".*?alt="(.*?)".*?"board-img".*?/>', re.S)
        film_act_pattern = re.compile(r'<dd>.*?"movie-item-info".*?<p.*?"star".*?>(.*?)</p>.*?"releasetime">(.*?)</p>', re.S)
        film_score_pattern = re.compile(r'<dd>.*?movie-item-number.*?<p.*?score.*?<i.*?integer.*?>(.*?)</i><.*?fraction.*?>(.*?)</i></p>', re.S)

        film_no = re.findall(film_no_pattern, response)
        film_info = re.findall(film_info_pattern, response)
        film_act = re.findall(film_act_pattern, response)
        film_score = re.findall(film_score_pattern, response)

        self.film_no = [i for i in film_no]
        self.film_info = [j for j in film_info]
        self.film_act = [k for k in film_act]
        self.film_score = [l for l in film_score]
        return True

    def get_images(self, url, name):
        pic_content = requests.get(url, self.headers).content
        pic_name = name + '.jpg'
        with open(pic_name, 'ab')as f:
            f.write(pic_content)

    def main(self):
        if self.num == 0:
            url = self.url
        elif self.num < 10:
            url = self.url + '?offset=' + str(10*(self.num))
        else:
            return
        time.sleep(random.randint(0, 3))
        res = self.get_hot_page(url)

        if res:
            print(self.film_no)
            print(self.film_info)
            # print(self.film_act)
            for i in range(len(self.film_no)):
                no = self.film_no[i] + '.'
                films_name = self.film_info[int(i) - 1][1]
                films_image_urls = self.film_info[int(i) - 1][0]
                actors = self.film_act[int(i) - 1][0].strip()
                show_time = self.film_act[int(i) - 1][1]
                films_score = self.film_score[int(i) - 1][0] + self.film_score[int(i) - 1][1]
                self.get_images(films_image_urls, films_name)

                # film = no +'.'+ ' ' + films_name + ' ' + actors + ' ' + show_time + '\n'
                film_params = [no, films_name, actors, show_time]
                films = ' '.join(film_params) + ' 评分: %s' % films_score + '\n'

                with open('maoyan_hot_top_100.txt', 'a')as f:
                    f.write(films)
            self.num += 1
        else:
            print("抓取网页信息失败!!!")

if __name__ == '__main__':
    spider = Spider()
    for _ in range(10):
        spider.main()