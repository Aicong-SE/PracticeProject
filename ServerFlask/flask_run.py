import json,requests
import sys

from flask import Flask, request, render_template
sys.path.append(sys.argv[0] + '../')
from flask_run import WXBizDataCrypt

app = Flask(__name__)

@app.route('/login', mothod=["GET",'POST'])
def login():
    if request.method == 'GET':
        return render_template('login/login.html') # 模板名，关键字传参
    elif request.method == 'POST':
        pass
        

@app.route('/wxlogin', method=['POST'])
def wxlogin():
    '''微信登录'''
    data = json.loads(request.get_data().decode('utf-8')) # 将前端Json数据转为字典
    appID = 'appID' # 开发者关于微信小程序的appID
    appSecret = 'appSecret' # 开发者关于微信小程序的appSecret
    code = data['platCode'] # 前端POST过来的微信临时登录凭证code
    encryptedData = data['platUserInfoMap']['encryptedData']
    iv = data['platUserInfoMap']['iv']
    req_params = {
        'appid': appID,
        'secret': appSecret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'
    response_data = requests.get(wx_login_api, params=req_params) # 向API发起GET请求
    resData = response_data.json()
    openid = resData ['openid'] # 得到用户关于当前小程序的OpenID
    session_key = resData ['session_key'] # 得到用户关于当前小程序的会话密钥session_key

    pc = WXBizDataCrypt(appID, session_key) #对用户信息进行解密
    userinfo = pc.decrypt(encryptedData, iv) #获得用户信息
    print(userinfo)

    '''下面部分是通过判断数据库中用户是否存在来确定添加或返回自定义登录态（若用户不存在则添加；若用户存在，返回用户信息）'''

    return json.dumps({"code": 200, "msg": "登录成功", "userinfo": userinfo}, indent=4, sort_keys=True, default=str, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
