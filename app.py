from flask import Flask, request, render_template, redirect, url_for
import requests
import json
import base64
import random
import os
import time
from datetime import datetime

app = Flask(__name__)

def generate_random_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    telno = request.form['telno']
    parola = request.form['parola']
    kod = request.form['kod']
    
    headers = {
        'User-Agent': 'VodafoneMCare/2308211432 CFNetwork/1325.0.1 Darwin/21.1.0',
        'Content-Length': '83',
        'Connection': 'keep-alive',
        'Accept-Language': 'tr_TR',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'm.vodafone.com.tr',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    random_ip = generate_random_ip()
    url = 'https://m.vodafone.com.tr/maltgtwaycbu/api/'
    
    data = {
        'context': 'e30=',
        'username': telno,
        'method': 'twoFactorAuthentication',
        'password': parola
    }
    
    response = requests.post(url, headers=headers, data=data)
    proid = response.json().get('process_id')
    
    if proid is None:
        return "Şifre veya Numara Yanlış❌", 400
    
    veri = {
        'langId': 'tr_TR',
        'clientVersion': '17.2.5',
        'reportAdvId': '0AD98FF8-C8AB-465C-9235-DDE102D738B3',
        'pbmRight': '1',
        'rememberMe': 'true',
        'sid': proid,
        'otpCode': kod,
        'platformName': 'iPhone'
    }
    
    base64_veri = base64.b64encode(json.dumps(veri).encode('utf-8'))
    
    data2 = {
        'context': base64_veri,
        'grant_type': 'urn:vodafone:params:oauth:grant-type:two-factor',
        'code': kod,
        'method': 'tokenUsing2FA',
        'process_id': proid,
        'scope': 'ALL'
    }
    
    response2 = requests.post(url, headers=headers, data=data2)
    
    o_head = {
        'Accept': 'application/json',
        'Language': 'tr',
        'ApplicationType': '1',
        'ClientKey': 'AC491770-B16A-4273-9CE7-CA790F63365E',
        'sid': proid,
        'Content-Type': 'application/json',
        'Content-Length': '54',
        'Host': 'm.vodafone.com.tr',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.10.0',
        'X-Forwarded-For': random_ip
    }
    
    return render_template('result.html', proid=proid, headers=o_head)

@app.route('/redirect', methods=['POST'])
def redirect_to():
    sec = request.form['sec']
    if sec == '1':
        return redirect('https://t.me/freeinternetv1/')
    elif sec == '2':
        return redirect('https://t.me/freeinternetv1/')
    else:
        return "Geçersiz seçim", 400

if __name__ == '__main__':
    app.run(debug=True)