# rest-aed-open-data-py

## eYACHO/GEMBA Note向けRESTサーバー

AEDオープンデータプラットフォーム([https://hatsunejournal.azurewebsites.net/w8/AEDOpendata/](https://hatsunejournal.azurewebsites.net/w8/AEDOpendata/))は、各自治体が公開するAEDデータや、設置者、地域の方から投稿されたAEDデータを統合して各種情報をREST/JSON形式で取得するAPIを無償で公開している。  

このサンプルのRESTサーバーは、AEDオープンデータプラットフォームが提供するAPIにアクセスして、指定した地域でのAEDの設置情報を株式会社MetaMoJiのデジタルノートアプリケーションeYACHOおよびGEMBA Noteが利用できるようにするRESTサーバーである。

### Pythonをインストールする

[https://www.python.org/downloads/](https://www.python.org/downloads/)からPythonをインストールする。

### 必要なパッケージのインストール

コマンドプロンプト上で、次のコマンドを実行し、必要なPythonのパッケージをインストールする。

```bash
pip install -r requirements.txt
```

### サーバーを起動する

コマンドプロンプトから次のコマンドを実行し、サーバーを起動する。

開発版（ソースコード編集内容が自動的に反映される）:

```bash
uvicorn main:app --reload
```

本番環境:

```bash
uvicorn main:app
```

コマンドの説明:

| コマンドの要素 |  説明  |
| ---- | ---- |
|  uvicorn  | FastAPIベースの非同期Python Webアプリケーションを実行する |
|  main:app  | Pythonファイルmain.pyの中で、FastAPIが生成する変数がapp |
|  --reload  | 実行中にソースコードが変更されたとき、サーバーが自動的にリロードされる |

デフォルトのポート番号は8000。  
ポート番号を指定するときは --port [ポート番号] を後ろに付与する。

### サーバーへアクセスする

Webブラウザを開き、次のURLへアクセスする（ポート番号が8000の場合）。

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

トップページが現れる。

### 環境件数

このサーバーは起動時に環境変数を参照する。環境変数は .envファイルに設定されている。

|  環境変数名 |  説明  |
| ---- | ---- |
| AED_REST_URL  | AEDオープンデータ REST APIへアクセスするルートURL |
| AED_PIN_MARK  | 地図上のピンの形状 |
| AED_PIN_SIZE  | 地図上のピンのサイズ |

### REST APIs

このサーバーが提供するREST APIエンドポイントは、ある定型的なJSON構造を返却する。その構造は、株式会社MetaMoJiの製品 **eYACHO** および **GEMBA Note**の開発者オプションのアグリゲーション検索条件を構成する **RESTコネクタ** の仕様に基づく。

REST用アグリゲーションの出力構造：

```bash
{
   'keys': ['key1', 'key2', ... 'keyN'], # recordsの中で用いるキーの一覧
   'records': [
       {'key1': value-11, 'key2': value-21, ... 'keyN': value-N1}, 
       {'key1': value-12, 'key2': value-22, ... 'keyN': value-N2}, 
       ...,
       {'key1': value-1m, 'key2': value-2m, ... 'keyN': value-Nm}, 
   ],
   'message': エラーメッセージ or null(success)
}
```

#### /aed_list (POSTメソッド)

指定した緯度と経度からその地点の天気と気温の予測データを1週間分（1時間ごと）取得する。

リクエストボディ（JSON）の構造：

|  キー |  説明  |
| ---- | ---- |
|  pref | 都道府県名（必須） |
|  city | 市町村名（必須）|

レスポンスの仕様:

|  キー  | 説明  |
| ---- | ---- |
| id | 場所のID |
| mapLocation | 緯度経度 |
| LocationName | 名称 |
| Prefecture | 都道府県名 |
| City | 市町村名 |
| AddressArea | アドレス |
| pinMark | ピンの形状 |
| pinSize | ピンのサイズ |

レスポンス例:

```bash
{
  'keys': ['id', 'mapLocation', 'LocationName', 'Prefecture', 'City', 'AddressArea', 'pinMark', 'pinSize'], 
  'records': [
    {
      'id': 40913, 
      'mapLocation': '{"la": 33.99130696, "lo": 134.5341754}', 
      'LocationName': '徳島市多家良中央コミュニティーセンター',
      'Prefecture': '徳島県', 'City': '徳島市', 
      'AddressArea': '多家良町小路地10', 
      'pinMark': 'pin', 'pinSize': 10
    },
    ...
  ],
  'message': null
}
```

### 更新履歴

- 2024-12-04 - 初回リリース
