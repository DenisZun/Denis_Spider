import re

url = "http://sdkpy.zqgame.com/3002/316/323/pay_notice"
url_01 = "https://www.google.com"
url_02 = "http://uni.notice.zqgame.com/3002/316/323/pay_notice"

content = 'Hello 1234567 World_This is a Sentence Sweet Heart'

res_01 = re.match(r'^Hello\s(\d+)\sWorld', content)

# res = re.match(r'[a-zA-Z]+://[^\s]*', url_02).group()
# print(res_01.group())
# print(res_01.group(1))

# =======================
# 贪婪与非贪婪
# =======================

# 贪婪模式,.*尽量匹配尽可能多的字符
res_02 = re.match(r'^He.*(\d+).*Heart$', content)
# print(res_02)
# print(res_02.group(1))

# 非贪婪模式,用?取消贪婪模式,尽可能匹配少的字符
res_03 = re.match(r'^He.*?(\d+).*Heart$', content)
# print(res_03)
# print(res_03.group(1))

url_wb = "http://weibo.com/comment/denis"
ret_01 = re.match(r'http.*?comment/(.*)', url_wb)
ret_02 = re.match(r'http.*?comment/(.*?)', url_wb)

# print(ret_01.group())
# print(ret_01.group(1))
# print(ret_01.group(2))

# print(ret_02.group())
# print(ret_02.group(1))

# =======================
# 匹配多行字符
# =======================
content = '''Hello 1234567 World_This is
a Sentence Sweet Heart
'''
content_01 = 'Hello 1234567 World_This is a Sentence Sweet Heart'

# res_04 = re.match(r'^He.*?(\d+).*?Heart$', content)
res_05 = re.match(r'^He.*?(\d+).*?Heart$', content_01)

# 直接匹配会报错
# AttributeError: 'NoneType' object has no attribute 'group'
# print(res_04.group())

# 这个时候应该用修饰符进行性多行匹配
# re.S匹配多行文字
res_04 = re.match(r'^He.*?(\d+).*?Heart$', content, re.S)
# print(res_04.group())

# 匹配单行并不会报错
# print(res_05.group())

h5_data = """
        <div id="songs-list">
        <h2 class="title">经典老歌</h2>
        <p class="introduction">经典老歌列表</p>
        <ul id="list" class="list-group">
            <li data-view="2">一路有你</li>
            <li data-view="7">
                <a href="/2.mp3" singer="罗文">小李飞刀</a>
            </li>
            <li data-view="7">
                <a href="/3.mp3" singer="张国荣">似水流年</a>
            </li>
            <li data-view="4" class="active">
                <a href="/4.mp3" singer="beyond">光辉岁月</a>
            </li>
            <li data-view="6">
                <a href="/5.mp3" singer="许冠杰">半斤八两</a>
            </li>
            <li data-view="5">
                <a href="/6.mp3" singer="陈百强">念亲恩</a>
            </li>
            <li data-view="5">
                <a href="/7.mp3" singer="梅艳芳">女人花</a>
            </li>
        </ul>
    </div>
    """

# <li.*?active.*?singer="(.*?)">(.*?)</a>
# res_songs = re.search(r'<li.*?active.*?singer="(.*?)">(.*?)</a>', h5_data, re.S)

# res_songs = re.findall(r'<li.*?href="(.*?)".*?singer="(.*?)">(.*?)</a>', h5_data, re.S)
# ret_songs_01 = res_songs.group(1)
# ret_songs_02 = res_songs.group(2)
# print(ret_songs_01 + ' - ' + ret_songs_02)


# for song in res_songs:
#     print(song[2]+ ' - ' +song[1]+ ' - ' +song[0])


html = re.sub(r'<a.*?>|</a>', '', h5_data)
html_ret = re.findall(r'<li.*?>(.*?)</li>', html, re.S)

for ret in html_ret:
    print(ret.strip())

