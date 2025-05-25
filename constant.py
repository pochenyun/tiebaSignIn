# 请求头
headers_sign = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
}
success_flag = "success"
signed_flag = "signed"
fail_flag = "fail"
# 贴吧起始页面
index_url = "https://tieba.baidu.com/index.html"
# 从这个接口中获取关注的吧
attention_url = "https://tieba.baidu.com/f/like/mylike"
# 利用此接口进行签到
sign_url = "https://c.tieba.baidu.com/c/c/forum/sign"
# tbs
tbs_url = "https://tieba.baidu.com/dc/common/tbs"
# 尝试次数
attempt_total=3
# 颜色
GREEN = '\033[92m'  # 绿色
YELLOW = '\033[33m' # 黄色
RED = '\033[91m'    # 红色
RESET = '\033[0m'   # 重置颜色
