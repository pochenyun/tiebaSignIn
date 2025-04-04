import tieba_login
import tieba_signIn
from tieba_favorite import get_favorite

if __name__ == '__main__':
    # 获取cookie
    cookie = tieba_login.login()
    # 获取关注的吧
    favorites = get_favorite(cookie)
    # 签到
    tieba_signIn.sign(cookie, favorites)
