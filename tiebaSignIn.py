# 用到的包
import os
import random
import re
import time
import requests
import bs4

import constant
from constant import success_flag, fail_flag

from logger import logger


def login():
    bduss = os.getenv("BDUSS")
    ptoken = os.getenv("PTOKEN")
    if not bduss or not ptoken:
        logger.info("缺少必要的环境变量")
        exit(1)
    # 构建Cookie
    login_cookie = {
        "BDUSS": bduss,
        "PTOKEN": ptoken,
    }
    # 向贴吧首页发起GET请求，并禁止重定向
    req = requests.get(url=constant.index_url, headers=constant.headers_sign, cookies=login_cookie,
                       allow_redirects=False)
    # 从反馈的信息中对Cookie进行补齐
    for key in req.cookies.keys():
        login_cookie[key] = req.cookies[key]
    # 虽然上面禁止了重定向，但是status_code仍然是302，如果是200那说明BDUSS过期了
    if req.status_code == 301 or req.status_code == 302:
        # 重定向的目标地址
        pass_url = req.headers['Location']
        # 对目标地址发起请求，这里仍然会重定向
        req_pass = requests.get(url=pass_url, headers=constant.headers_sign, cookies=login_cookie,
                                allow_redirects=False)
        # 获取重定向的地址
        stoken_url = req_pass.headers['Location']
        # print(stoken_url)
        # 访问目标地址，获取STOKEN
        req_stoken = requests.get(url=stoken_url, headers=constant.headers_sign, cookies=login_cookie,
                                  allow_redirects=False)
        try:
            # 将STOKEN写入login_cookie
            login_cookie["STOKEN"] = req_stoken.cookies['STOKEN']
            # 带上login_cookie去签到
            run(login_cookie)
        except:
            pass
    else:
        print(req.status_code)


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


# 获取关注的吧
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


# 控制函数
def run(cookie):
    # 获取关注的吧
    favorites = get_favorite(cookie)
    logger.info(f"签到开始，一共有{len(favorites)}页，{len(favorites)}个吧要签到！")
    counts = {success_flag: 0, fail_flag: 0}
    # 创建一个随机数生成器
    rand_gen = random.Random()
    # 逐一签到，并停顿0.3-0.5秒
    for favorite in favorites:
        ret = client_sign(favorite, cookie)
        # 更新成功或失败计数
        counts[ret] = counts.get(ret) + 1
        # 生成随机休眠时间
        time.sleep(rand_gen.uniform(0.3, 0.5))
    logger.info(f"签到成功贴吧数量：{counts[constant.success_flag]}, 签到失败贴吧数量：{counts[constant.fail_flag]}")


# 签到模块
def client_sign(kw, cookie):
    # post请求需要的参数，kw指吧名
    data = {"ie": "utf-8", "kw": kw}
    # 带上参数对接口发起post请求，并将response处理成json格式
    res = requests.post(url=constant.sign_url, data=data, cookies=cookie, timeout=5).json()
    # 检查签到状态
    if res['no'] == 0:
        logger.info(kw + ',' + '签到成功！')
        return success_flag
    else:
        logger.info(kw + ',' + res['error'])
        return fail_flag
