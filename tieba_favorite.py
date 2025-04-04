import re
import bs4
import requests

import constant
from logger import logger


def get_favorite(cookie):
    # 将关注的吧存入列表并返回
    favorites = []
    # 获取页数
    pn_max = get_favorite_page_num(cookie)
    if pn_max == 0:
        logger.info("未获取贴吧信息")
        return favorites
    for i in range(1, pn_max + 1):
        # attention_url算是一个接口，在i贴吧查看关注的吧时可以看到
        req = requests.get(f"{constant.attention_url}?&pn={i}", headers=constant.headers_sign, cookies=cookie)
        # 调用bs4解析网页，需要预先安装lxml模块
        html = bs4.BeautifulSoup(req.text, 'lxml')
        # 从页面中检索关注的贴吧
        tieba_list = html.find('div', class_="forum_table").find_all("tr")[1:]
        # 将关注的贴吧直接添加到favorite中
        favorite_page = []
        for tieba in tieba_list:
            favorite_page.append(tieba.find('a', class_=None).get('title'))
        logger.info(f"在第{str(i)}页，获取到这些贴吧{favorite_page}")
        favorites.extend(favorite_page)
    return favorites


# 获取关注贴吧页面页数
def get_favorite_page_num(cookie):
    # attention_url算是一个接口，在i贴吧查看关注的吧时可以看到
    req = requests.get(url=constant.attention_url, headers=constant.headers_sign, cookies=cookie)
    # 调用bs4解析网页，需要预先安装lxml模块
    html = bs4.BeautifulSoup(req.text, 'lxml')
    # 返回导航链接
    links = html.find_all('a', href=True)
    # 提取pn后的数字
    pn_nums = []
    for link in links:
        match = re.search(r'pn=(\d+)', link['href'])
        if match:
            pn_nums.append(int(match.group(1)))
    # 获取最大的pn值，即尾页的数字
    if pn_nums:
        last_page = max(pn_nums)
        logger.info(f'尾页的数字是: {str(last_page)}')
        return last_page
    else:
        logger.info('未找到尾页信息')
        return 0
