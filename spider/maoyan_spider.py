import re
import random
import requests

# html = """
# <dd>
#     <i class="board-index board-index-7">7</i>
#     <a href="/films/1220713" title="新大头儿子和小头爸爸3：俄罗斯奇遇记" class="image-link" data-act="boarditem-click" data-val="{movieId:1220713}">
#       <img src="//ms0.meituan.net/mywww/image/loading_2.e3d934bf.png" alt="" class="poster-default" />
#       <img data-src="http://p1.meituan.net/movie/517fd5611a22ea9b498fb2dac3dcd1461033977.jpg@160w_220h_1e_1c" alt="新大头儿子和小头爸爸3：俄罗斯奇遇记" class="board-img" />
#     </a>
#     <div class="board-item-main">
#       <div class="board-item-content">
#         <div class="movie-item-info">
#             <p class="name"><a href="/films/1220713" title="新大头儿子和小头爸爸3：俄罗斯奇遇记" data-act="boarditem-click" data-val="{movieId:1220713}">新大头儿子和小头爸爸3：俄罗斯奇遇记</a></p>
#             <p class="star">
#                     主演：刘纯燕,董浩,鞠萍
#             </p>
#             <p class="releasetime">上映时间：2018-07-06</p>
#         </div>
#         <div class="movie-item-number score-num">
#             <p class="score"><i class="integer">8.</i><i class="fraction">6</i></p>
#         </div>
#
#       </div>
#     </div>
#
# </dd>
# """
# '''
# <dd>.*?board-index.*?>(.*?)</i>
# <dd>.*?board-index.*?>(.*?)</i>*?<img.*?data-src=(.*?)
#
# '''
# # 1.获取影片编号
# res = re.search(r'<dd>.*?board-index.*?>(.*?)</i>', html, re.S)
# print(res.group(1))
#
# # 2.获取电影图片,名称
# res_1 = re.search(r'<dd>.*?board-index.*?>.+</i>.*<img.*?data-src="(.*?)".*?alt="(.*?)".*?"board-img".*?/>', html, re.S)
# print(res_1.group(1), res_1.group(2))
#
# # 3.获取电影主演,以及上映时间
# res_2 = re.search(r'<dd>.*?"movie-item-info".*?<p.*?"star".*?>(.*?)</p>.*?"releasetime">(.*?)</p>', html, re.S)
# print(res_2.group(1).strip(), res_2.group(2))
#
# # 4.获取电影评分
# res_3 = re.search(r'<dd>.*?movie-item-number.*?<p.*?score.*?<i.*?integer.*?>(.*?)</i><.*?fraction.*?>(.*?)</i></p>', html, re.S)
# print(res_3.group(1)+res_3.group(2))


class Spider(object):
    """猫眼电影爬虫"""
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
            "Mozilla/5.0 (Macintosh;U;IntelMacOSX10_6_8;en-us) AppleWebKit/534.50(KHTML,likeGecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows;U;WindowsNT6.1;en-us) AppleWebKit/534.50 (KHTML,likeGecko) Version/5.1 Safari/534.50"
        ]
        self.headers = {
            "User-Agent": random.choice(self.user_agents)
        }
        self.url = "http://maoyan.com/board/7"

    def get_hot_page(self, url):
        ret = None
        res = requests.get(url, headers=self.headers)
        if res.status_code == 200:
            response = res.text
            ret = self.parse_page(response)
            return ret
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

    def get_images(self, url, name):
        pic_content = requests.get(url, self.headers).content
        pic_name = name + '.jpg'
        with open(pic_name, 'ab')as f:
            f.write(pic_content)

    def main(self):
        # print(html)
        self.get_hot_page(self.url)
        print(self.film_no)
        print(self.film_info)
        print(self.film_act)
        print(self.film_score)

        for i in self.film_no:
            film_id = i + '.'
            films_name = self.film_info[int(i) - 1][1]
            films_image_urls = self.film_info[int(i) - 1][0]
            actors = self.film_act[int(i) - 1][0].strip()
            show_time = self.film_act[int(i) - 1][1]
            films_score = self.film_score[int(i) - 1][0] + self.film_score[int(i) - 1][1]
            self.get_images(films_image_urls, films_name)

            film_params = [film_id, films_name, actors, show_time]
            films = ' '.join(film_params) + ' 评分: %s' % films_score + '\n'

            # film = i +'.'+ ' ' + films_name + ' ' + actors + ' ' + show_time + ' ' + '评分:' + films_score + '\n'

            with open('maoyan_hot.txt', 'a')as f:
                f.write(films)


if __name__ == '__main__':
    spider = Spider()
    spider.main()