#!/usr/bin/env python3
"""
EC2 診断用スクリプト
URL パターンとAPIエンドポイントの状況を確認する
"""
import os
import sys
import django
from django.conf import settings

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'runners_insight.settings')
django.setup()

from django.urls import get_resolver
from django.test import Client
import json

print("=== Runners' Insight ローカル診断スクリプト ===")
print()

# 1. URL パターン確認
print("1. 登録されているURLパターン:")
def show_urls(urllist, depth=0):
    for entry in urllist:
        pattern_str = str(entry.pattern)
        print('  ' * depth + pattern_str)
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

resolver = get_resolver()
show_urls(resolver.url_patterns)
print()

# 2. API エンドポイントテスト
print("2. APIエンドポイントテスト:")
client = Client()

# ヘルスチェック
try:
    response = client.get('/api/health/')
    print(f"  GET /api/health/ -> {response.status_code}")
    if response.status_code == 200:
        print(f"    Content: {response.content.decode()}")
except Exception as e:
    print(f"  GET /api/health/ -> ERROR: {e}")

# 動画アップロード（GET）
try:
    response = client.get('/api/videos/upload/')
    print(f"  GET /api/videos/upload/ -> {response.status_code}")
    if response.status_code != 404:
        print(f"    Content: {response.content.decode()[:100]}...")
except Exception as e:
    print(f"  GET /api/videos/upload/ -> ERROR: {e}")

# 動画アップロード（POST - 簡易テスト）
try:
    response = client.post('/api/videos/upload/', {})
    print(f"  POST /api/videos/upload/ (empty) -> {response.status_code}")
    if response.status_code != 404:
        print(f"    Content: {response.content.decode()[:100]}...")
except Exception as e:
    print(f"  POST /api/videos/upload/ -> ERROR: {e}")

print()

# 3. 設定確認
print("3. 設定確認:")
print(f"  DEBUG: {settings.DEBUG}")
print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"  INSTALLED_APPS with 'api': {'api' in settings.INSTALLED_APPS}")
print()

# 4. ファイル存在確認
print("4. 重要ファイル存在確認:")
files_to_check = [
    'api/urls.py',
    'api/views.py', 
    'runners_insight/urls.py',
    'manage.py'
]

for file_path in files_to_check:
    exists = os.path.exists(file_path)
    print(f"  {file_path}: {'存在' if exists else '不在'}")
    if exists and file_path == 'api/urls.py':
        with open(file_path, 'r') as f:
            content = f.read()
            has_upload = 'videos/upload' in content
            print(f"    -> 'videos/upload' パターン: {'有' if has_upload else '無'}")

print()
print("=== 診断完了 ===")
