from subprocess import call
from urllib.parse import urlencode, unquote
from pyquery import PyQuery as pq
import sys
import httplib2
import re

### 設定 ###

# ニコニコ動画のメールアドレスとパスワード
# パスワードは端末から入力しても良い。←の意味がわからなければここに書く。
MAIL = 'nekoneko.myaomyao@gmail.com'
PASS = ''

# ダウンロードした動画は消すか(Trueなら消す)
DELETE_MOV = False

# ログがウザいときはFalseにする
VERBOSE_LOG = True

############

if len(sys.argv) < 2:
    print('動画のID入力してね:sm444444みたいなやつ。たとえ動画のID間違えても無理矢理続行するよ')
    exit()

FLV_ID = sys.argv[1]

if PASS == '':
    if len(sys.argv) < 3:
        print('パスワード入力してね')
        exit()
    PASS = sys.argv[2]
class x:
    def write(self, string):
        pass
    def flush(self):
        pass

if not VERBOSE_LOG:
    sys.stdout = x()


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "ja,en-US;q=0.8,en;q=0.6,zh-TW;q=0.4,zh;q=0.2",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "KaeruKun Browser"
}

LOGIN_BEFORE_URI = 'https://account.nicovideo.jp/login'

LOGIN_URI = 'https://secure.nicovideo.jp/secure/login'
FORM_BODY = {"mail_tel":MAIL,"password":PASS}

GET_FLV_URI = "http://flapi.nicovideo.jp/api/getflv/{0}".format(FLV_ID)
GET_WATCH_URI = "http://www.nicovideo.jp/watch/{0}".format(FLV_ID)

FLV_ID = sys.argv[1]
RIGHT_ARROW = '->'

def set_co(response_cookie):
    set_cookies = re.split(r'user_session=', response['set-cookie'])
    print(set_cookies)
    for cookie in set_cookies:
        if cookie.startswith('user_session'):
            return 'user_session=' + cookie
    raise Exception()

ht = httplib2.Http()

print("-"*50) ####################################################################
print("ログイン処理", "GET", RIGHT_ARROW, LOGIN_BEFORE_URI)

ht.add_credentials('mail_tel', 'password')
response, content = ht.request(uri=LOGIN_BEFORE_URI, method='GET')

print(response)

print("-"*50) ####################################################################
print("ログイン処理", "POST", RIGHT_ARROW, LOGIN_URI)
response, content = ht.request(uri=LOGIN_URI, method='POST', body=urlencode(FORM_BODY), headers=headers, redirections=10)

print(response)
print(content)

print("-"*50) ####################################################################

print("クッキーをセット", "---", RIGHT_ARROW)
headers['Cookie'] = set_co(response['set-cookie'])

print("-"*50) ####################################################################

print("ダウンロードURI取得処理", "GET", RIGHT_ARROW, GET_FLV_URI)
response, content = ht.request(uri=GET_FLV_URI, method='GET', headers=headers)
print(response)
print(content)

print("-"*50) ####################################################################

print("URI変換処理", "---", RIGHT_ARROW)
content_data = content.decode()
content_data = re.sub(r'^.*&url=', '', content_data)
content_data = re.sub(r'&ms=.*$', '', content_data)
download_uri = unquote(content_data)

def set_co(response_cookie):
    set_cookies = re.split(r', ', response['set-cookie'])
    print(set_cookies)
    for cookie in set_cookies:
        if cookie.startswith('nicohistory='):
            return cookie
    raise Exception()

print("-"*50) ####################################################################

print("ダウンロード前閲覧処理", "GET", RIGHT_ARROW, GET_WATCH_URI)
response, content = ht.request(uri=GET_WATCH_URI, method='GET', headers=headers)
print(response)
nodes = pq(content.decode())
title_text = nodes('title').text()

print("-"*50) ####################################################################

print("クッキーをセット", "---", RIGHT_ARROW)
headers["Cookie"] = set_co(response["set-cookie"]) + "; " + headers["Cookie"]

print("-"*50) ####################################################################

print("ダウンロード開始", "GET", RIGHT_ARROW, download_uri)
response, content = ht.request(uri=download_uri, method='GET', headers=headers)
print(response)

print("-"*50)

print("ダウンロード完了。動画ファイル作成処理", "---", RIGHT_ARROW)
# because of dull to distinct extensions
d_name = title_text + '.mp4'
conv_name = title_text + '.mp3'
down = open(d_name, 'wb')
down.write(content)

print("-"*50)
call(['ffmpeg', '-i', d_name, conv_name, '-y'])
if DELETE_MOV:
    call(['rm', '--', d_name])

