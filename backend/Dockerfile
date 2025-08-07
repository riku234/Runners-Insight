# 1. ベースイメージを選択
FROM python:3.10-slim

# 2. 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. 作業ディレクトリを設定
WORKDIR /app

# 4. OSのパッケージをインストール (本番用に最適化)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    # PostgreSQLに接続するために必要
    postgresql-client \
    # C拡張モジュールを持つライブラリのビルドに必要
    build-essential \
    # OpenCV (headless) の実行に必要最小限のライブラリ
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. requirements.txtをコピーして、Pythonライブラリをインストール
#    この段階で実行することで、コード変更時のビルドキャッシュを有効活用する
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 6. アプリケーションのコードをコピー
COPY . /app
