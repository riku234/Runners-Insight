FROM python:3.9-slim

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgomp1 \
        libgthread-2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# 静的ファイルを収集
RUN python manage.py collectstatic --noinput

# ポートを公開
EXPOSE 8000

# Gunicornでアプリケーションを起動
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "runners_insight.wsgi:application"]
