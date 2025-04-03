# 贴吧名字存储文件
file_path = "tieba.txt"
# 请求头
headers_sign = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
}
success_flag = "success"
fail_flag = "fail"
# 贴吧起始页面
index_url = "https://tieba.baidu.com/index.html"
# 从这个接口中获取关注的吧
attention_url = 'http://tieba.baidu.com/f/like/mylike'
# 利用此接口进行签到
sign_url = 'https://tieba.baidu.com/sign/add'
