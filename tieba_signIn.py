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
    def do_sign(fav_list, counts, attempt):
        retry_favorites = []
        for favorite in fav_list:
            sign_str = f"kw={favorite}tbs={tbs}tiebaclient!!!"
            sign_md5 = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
            data = {
                "kw": favorite,
                "tbs": tbs,
                "sign": sign_md5
            }
            ret = client_sign(data, cookie)
            if ret == success_flag:
                counts[success_flag] += 1
            elif ret == signed_flag:
                counts[signed_flag] += 1
            elif ret == fail_flag:
                counts[fail_flag] += 1
                retry_favorites.append(favorite)
            time.sleep(rand_gen.uniform(0.3, 0.5))
        if retry_favorites and attempt < constant.attempt_total:
            logger.info(f"第{attempt + 1}次重试 {len(retry_favorites)} 个失败的贴吧")
            do_sign(retry_favorites, counts, attempt + 1)
        # 缓一下重连
        time.sleep(rand_gen.uniform(5, 10))

    # 获取tbs
    tbs = get_tbs(cookie)
    # 签到开始
    logger.info(f"签到开始，一共有{len(favorites)}页，{len(favorites)}个吧要签到！")
    counts = {
        success_flag: 0,
        signed_flag: 0,
        fail_flag: 0,
    }
    # 创建一个随机数生成器
    rand_gen = random.Random()
    # 逐一签到，并停顿0.3-0.5秒
    do_sign(favorites, counts, 1)
    logger.info(f"{constant.GREEN}签到成功贴吧数量：{counts.get(success_flag)}{constant.RESET}, "
                f"{constant.YELLOW}签到过贴吧数量：{counts.get(signed_flag)}{constant.RESET}, "
                f"{constant.RED}签到失败贴吧数量：{counts.get(fail_flag)}{constant.RESET}")


# 获取tbs
def get_tbs(cookie):
    attempt = 0
    rand_gen = random.Random()
    
    while attempt < constant.attempt_total:
        try:
            req = requests.get(constant.tbs_url, headers=constant.headers_sign, cookies=cookie)
            tbs_url_res = json.loads(req.text)
            if tbs_url_res["is_login"] == 1:
                logger.info("获取TBS成功")
                return tbs_url_res["tbs"]
            else:
                logger.warning(f"第 {attempt + 1} 次获取TBS失败")
        except Exception as e:
            logger.error(f"第 {attempt + 1} 次获取TBS出错: {str(e)}")
        
        attempt += 1
        if attempt < constant.attempt_total:
            sleep_time = rand_gen.uniform(3, 6)  # 随机等待3-6秒
            logger.info(f"等待 {sleep_time:.1f} 秒后进行第 {attempt + 1} 次重试")
            time.sleep(sleep_time)
    
    logger.error(f"获取TBS失败，已重试 {constant.attempt_total} 次")
    raise Exception("登录失败")


# 签到模块
def client_sign(data, cookie):
    # 带上参数对接口发起post请求，并将response处理成json格式
    res = requests.post(url=constant.sign_url, data=data, cookies=cookie, timeout=5).json()
    # 检查签到状态
    if res['error_code'] == 0 or 'user_info' in res:
        logger.info(f"{data.get('kw')}吧，签到成功！")
        return success_flag
    elif res['error_code'] == "160002":
        logger.info(f"{data.get('kw')}吧，已经签到过了！")
        return signed_flag
    else:
        logger.info(f"{data.get('kw')}吧，签到失败！")
        logger.info(f"失败原因：{str(res)}")
        return fail_flag
