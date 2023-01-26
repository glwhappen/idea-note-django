from datetime import datetime

from simplejwt.jwt import Jwt, decode

SECRET_KEY = '123456'
# token 有效时间 时 分 秒
TOKEN_LIFETIME = 12 * 60 * 60


class JwtUtils:
    @staticmethod
    def get_token(payload):
        time_now = int(datetime.now().timestamp())
        valid_to = time_now + TOKEN_LIFETIME
        jwt = Jwt(secret=SECRET_KEY, payload=payload, valid_to=valid_to)
        return jwt.encode()

    @staticmethod
    def get_payload(token):
        return decode(SECRET_KEY, token)[1]


    @staticmethod
    def is_timeout(payload):
        time_now = int(datetime.now().timestamp())
        if payload['exp'] < time_now:
            return True
        else:
            return False


if __name__ == '__main__':
    token = JwtUtils.get_token({'username': 'admin'})
    print(token)
    payload = JwtUtils.get_payload(token)
    print(payload)
    print(JwtUtils.is_timeout(payload))