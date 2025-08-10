import os
import time
import random
import requests

import constant
from logger import logger


def login():
    bduss = os.getenv("BDUSS")
    ptoken = os.getenv("PTOKEN")
    if not bduss or not ptoken:
        logger.info("缺少必要的环境变量")
        exit(1)

    login_cookie = {
        "BDUSS": bduss,
        "PTOKEN": ptoken,
    }

    # 向贴吧首页发起GET请求
    req = make_request(constant.index_url, login_cookie)
    if req is None:
        logger.error("登录失败：无法访问贴吧首页")
        exit(1)

    # 从反馈的信息中对Cookie进行补齐
    for key in req.cookies.keys():
        login_cookie[key] = req.cookies[key]

    if req.status_code in (301, 302):
        pass_url = req.headers['Location']
        req_pass = make_request(pass_url, login_cookie)
        if req_pass is None:
            logger.error("登录失败：无法完成重定向")
            exit(1)

        stoken_url = req_pass.headers['Location']
        req_stoken = make_request(stoken_url, login_cookie)
        if req_stoken is None:
            logger.error("登录失败：无法获取STOKEN")
            exit(1)

        try:
            login_cookie["STOKEN"] = req_stoken.cookies['STOKEN']
            logger.info("登录成功")
            return login_cookie
        except KeyError as e:
            logger.error(f"键值不存在: {e}")
        except Exception as e:
            logger.error(f"登录过程中出错: {e}")
    else:
        logger.error(f"错误码：{req.status_code}, 错误信息：{req.text}")
        exit(1)


def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
    ]
    return random.choice(user_agents)


def get_headers():
    return {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }


def make_request(url, cookies, max_retries=5):
    for attempt in range(max_retries):
        try:
            # 随机延时0.5-2秒
            time.sleep(random.uniform(0.5, 2))
            headers = get_headers()
            response = requests.get(
                url=url,
                headers=headers,
                cookies=cookies,
                allow_redirects=False,
                timeout=10
            )
            if response.status_code != 403:
                return response
            logger.warning(f"第{attempt + 1}次请求返回403，正在重试...")
        except requests.exceptions.RequestException as e:
            logger.error(f"请求出错: {str(e)}")
        # 重试前等待时间递增
        if attempt < max_retries - 1:
            time.sleep((attempt + 1) * 2)
    return None
