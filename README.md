## requirements.txt の中身

fastapi==0.70.0
uvicorn==0.14.0
fastapi_csrf_protect==0.2.1

### fastapi と mongodb を接続するためのパッケージ motor をインストール

motor==2.5.1
PyJWT==2.3.0
passlib==1.7.4
bcrypt==3.2.0

### 環境変数を扱うときに必要になる

python-decouple==3.3
pymongo==3.12.1
dnspython==2.1.0
gunicorn==20.1.0

## MongoDB 設定

.env ファイルを作成し、以下の MONGO_API_KEY 変数を定義します。
MongoDB の username、password、db_name は、各自変更すること。

MONGO_API_KEY=mongodb+srv://<username>:<password>@fastapi.gxovn.mongodb.net/<db_name>?retryWrites=true&w=majority
