#
# [FILE] aed_opendata.py
#
# [DESCRIPTION]
#  AEDオープンデータプラットフォームAPIからAEDの設置情報を取得する関数を定義する
#
# [NOTES]
#  AEDオープンデータプラットフォームについてはこちらを参照のこと：https://hatsunejournal.azurewebsites.net/w8/AEDOpendata/
#
import os
import json
import requests
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()

# 環境変数からAEDオープンデータプラットフォームのREST URLを取得する
restURL = os.environ.get("AED_REST_URL")
if restURL == None:
    print("[ERROR] AED_REST_URL not specified.")
    restURL = ""

# ピンの設定
pinMark = os.environ.get("AED_PIN_MARK")
if pinMark == None:
    print("[WARNING] AED_PIN_MARK not specified.")
    pinMark = "pin"

pinSize = os.environ.get("AED_PIN_SIZE")
if pinSize == None:
    print("[WARNING] AED_PIN_SIZE not specified.")
    pinSize = 10
else:
    pinSize = int(pinSize)
    
#
# [FUNCTION] getAEDInfo()
#
# [DESCRIPTION]
#  指定した都道府県名と市町村名からAED設置場所の情報を収集する
#
# [INPUTS]
#  prefecture - 都道府県名
#  city - 市町村名
#
# [OUTPUTS]
#  成功: {'status':'ok', 
#        'aed': [{'id':69956, 'mapLocation':{'lo':..,.'la':...}, 'LocationName':'三井住友銀行 品川支店'. ...},...], 
#        'message': null}
#  失敗: {'status':"error", 'aed': [], 'message': '[AED OPEN DATA] AED not found'}
#
# [NOTES]
#  REST APIアクセスの例:
#   https://aed.azure-mobile.net/api/aedinfo/東京都/港区
#
def getAEDInfo(prefecture, city):
    # 返り値の初期値
    retVal = {'status':'error', 'aed': [], 'message': '[AED OPEN DATA] AED not found'}

    # アクセスするURLを生成する
    url = restURL + "/" + prefecture + "/" + city
    print("[URL]", url)

    # Header
    headers = { 'content-type': 'application/json' }

    # URLにGETメソッドでアクセスする
    result = None
    try:
        response = requests.get(url, headers=headers)
        result = response.json()
    except requests.exceptions.RequestException as err:
        print("[Server Connection Error]:", err)

    if result != None:
        infoList = []
        for aed in result:
            info = {}
            geolocation = {}
            info['id'] = aed['Id']
            geolocation['la'] = aed['Latitude']
            geolocation['lo'] = aed['Longitude']
            info['mapLocation'] = json.dumps(geolocation)
            info['LocationName'] = aed['LocationName']
            info['Prefecture'] = aed['Perfecture'] # Perfectureは誤字
            info['City'] = aed['City']
            info['AddressArea'] = aed['AddressArea']
            info['pinMark'] = pinMark
            info['pinSize'] = pinSize
            infoList.append(info)
        retVal['aed'] = infoList
    else:
        return retVal

    retVal['status'] = 'ok'
    retVal['message'] = None

    return retVal
#
# HISTORY
# [1] 2024-12-04 - Initial version
#