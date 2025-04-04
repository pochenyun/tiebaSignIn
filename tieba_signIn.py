# 用到的包
import hashlib
import json
import random
import time

import requests

import constant
from constant import success_flag, signed_flag, fail_flag
from logger import logger


def sign(cookie, favorites):
    # 获取tbs
    tbs = get_tbs(cookie)
    # 签到开始
    logger.info(f"签到开始，一共有{len(favorites)}页，{len(favorites)}个吧要签到！")
    counts = {success_flag: 0, signed_flag: 0, fail_flag: 0}
    # 创建一个随机数生成器
    rand_gen = random.Random()
    # 逐一签到，并停顿0.3-0.5秒
    for favorite in favorites:
        # 移动端md5加密后的十六进制处理
        sign_str = f"kw={favorite}tbs={tbs}tiebaclient!!!"
        sign_md5 = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
        # post请求需要的参数，kw指吧名
        data = {
            "kw": favorite,
            "tbs": tbs,
            "sign": sign_md5
        }
        ret = client_sign(data, cookie)
        # 更新成功或失败计数
        counts[ret] = counts.get(ret) + 1
        # 生成随机休眠时间
        time.sleep(rand_gen.uniform(0.3, 0.5))
    logger.info(f"签到成功贴吧数量：{counts[constant.success_flag]}, 签到失败贴吧数量：{counts[constant.fail_flag]}")


# 获取tbs
def get_tbs(cookie):
    req = requests.get(constant.tbs_url, headers=constant.headers_sign, cookies=cookie)
    tbs_url_res = json.loads(req.text)
    if tbs_url_res["is_login"] == 1:
        logger.info("获取TBS成功")
        return tbs_url_res["tbs"]
    else:
        logger.info("获取TBS失败")
        raise Exception("登录失败")


# 签到模块
def client_sign(data, cookie):
    # 带上参数对接口发起post请求，并将response处理成json格式
    res = requests.post(url=constant.sign_url, data=data, cookies=cookie, timeout=5).json()
    # 检查签到状态
    if res['error_code'] == 0:
        logger.info(f"{data.get("kw")}吧，签到成功！")
        return success_flag
    elif res['error_code'] == "160002":
        logger.info(f"{data.get("kw")}吧，已经签到过了！")
        return signed_flag
    else:
        logger.info(f"{data.get("kw")}吧，签到失败！")
        logger.info(f"失败原因：{str(res)}")
        return fail_flag
