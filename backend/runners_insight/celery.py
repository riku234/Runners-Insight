# backend/runners_insight/celery.py

import os
from celery import Celery

# Djangoのsettingsモジュールを設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'runners_insight.settings')

# Celeryアプリケーションのインスタンスを作成
app = Celery('runners_insight')

# Django設定ファイルからCeleryの設定を読み込む
app.config_from_object('django.conf:settings', namespace='CELERY')

# Djangoアプリケーションのタスクを自動で検出する
app.autodiscover_tasks()
