import urllib.request
from lxml import etree
from time import sleep
from pathlib import *
import Translator

# 配置用户代理
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

# 全集页面
url = 'https://mp.weixin.qq.com/s/n3bZZaMpH7kv_Yu0ieEW1g'

# 定制 Request 对象
request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)

# 读取网页内容（二进制）然后解码
content = response.read().decode('utf-8')

# 获取所有需要下载的页面
tree = etree.HTML(content)
sub_url = tree.xpath('//div[contains(@class,"rich_media_content")]//a/@href')
sub_name = tree.xpath('//div[contains(@class,"rich_media_content")]//a/text()')

# 翻译器
translator = Translator.Translator()

f = open('debug.txt', 'wt', encoding='utf-8')

n = len(sub_url)
cn_name = ''
for i in range(n):
    url = sub_url[i]
    last_name = cn_name
    name = sub_name[i]

    if name[-1] == '）':
        cn_name = name[10:-3]
    else:
        cn_name = name[10:]

    # 将同一个作品放到同一个文件夹里
    if last_name != cn_name:
        j = 1
        count = 0
        en_name = translator.translate(cn_name)
        n_dir = Path('./' + en_name)
        n_dir.mkdir()

    print(last_name, cn_name)

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)

    # 获得所有图片 url
    content = response.read().decode('utf-8')
    tree = etree.HTML(content)
    img_list = tree.xpath('//div[contains(@class,"rich_media_content")]//img/@data-src')
    count = count + len(img_list)

    for img in img_list:
        fn = './' + en_name + '/' + str(j) + '.jpg'
        j = j + 1
        urllib.request.urlretrieve(url=img, filename=fn)
        print(fn + ' downloaded.')

    files = [str(f) for f in n_dir.iterdir() if Path(f).is_file()]
    if len(files) < count:
        f.write(en_name + ' is not complete!')
        
    sleep(5)

f.close()