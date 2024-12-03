#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [FILE] main.py
#
# [DESCRIPTION]
#  AEDオープンデータプラットフォームのAPIを利用したRESTメソッドを定義する
# 
# [NOTES]
#
import sys
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.aed_opendata import getAEDInfo
    
app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#
# [FUNCTION] is_reload_enabled()
#
# [DESCRIPTION]
#  実行するコマンドに--reloadが含まれるか判定する
#
# [INPUTS] None
#
# [OUTPUTS]
#  True: 含まれる False: 含まれない
#
# [NOTES]
#  Trueの場合はデバッグ実行とみなし、JSONデータをコンソール上に表示する
#
def is_reload_enabled():
    return "--reload" in sys.argv
#
# HISTORY
# [1] 2024-12-04 - Initial version
#

#
# GET Method
# End Point: /
#
# [DESCRIPTION]
#  トップページを開く
#
# [INPUTS]
#  request - リクエスト
# 
# [OUTPUTS]
# 
# [NOTES]
#  Web画面上に単に、"AED Open Data REST Server"と表示するのみ
#
@app.get("/", response_class=HTMLResponse)
async def topPage(request: Request):
    
    return templates.TemplateResponse("top.html", {"request": request, "title": "AED Open Data REST Server"})
#
# HISTORY
# [1] 2024-12-04 - Initial version
#

#
# GET Method
# End Point: /aed_list
#
# [DESCRIPTION]
#  都道府県名と市町村名からAEDが設置されている場所の情報を取得する
#
# [INPUTS] 
#  json_data - 都道府県名と市町村名を含むJSONデータ
# 
# [OUTPUTS]
# {
#   'keys': ['id', 'mapLocation', 'LocationName', 'Prefecture', 'City', 'AddressArea', 'pinMark', 'pinSize'], 
#   'records': [
#       {'id':69956, 'mapLocation':{'lo':..,.'la':...}, 'LocationName':'三井住友銀行 品川支店'. ...},  
#       {'id':68537, 'mapLocation':{'lo':..,.'la':...}, 'LocationName':'みずほ銀行　高輪台支店'. ...},  
#       ...
#   ],
#   'message': <エラーメッセージ>
# }
# 
# [NOTES]
# 
#
@app.post("/aed_list")
def getAEDList(json_data: dict): 
    results = {'keys':[], 'records':[], 'message':'都道府県名あるいは市町村名がありません'};
  
    # 都道府県名の取得
    pref = json_data['pref']
    # 市町村名の取得
    city = json_data['city']

    # 緯度と経度の存在チェック
    if pref == None or city == None or pref == '' or city == '':
        return results

    results['keys'] = ['id', 'mapLocation', 'LocationName', 'Prefecture', 'City', 'AddressArea', 'pinMark', 'pinSize']

    info = getAEDInfo(pref, city)

    results['records'] = info['aed']
    results['message'] = info['message']
  
    if is_reload_enabled():
        print("[JSON]", results)

    return results
#
# HISTORY
# [1] 2024-12-04 - Initial version
#