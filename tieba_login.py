import os

import requests

import constant
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
            return login_cookie
        except KeyError as e:
            logger.error(f"键值不存在: {e}")
        except Exception as e:
            logger.error(f"登录过程中出错: {e}")
    else:
        logger.info(f"错误码：{req.status_code}, 错误信息：{req.text}")
