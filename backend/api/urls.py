from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    # モック/テスト用エンドポイント
    path('analysis/mock/', views.mock_video_analysis, name='mock_video_analysis'),
    path('advice/generate/', views.mock_generate_advice, name='mock_generate_advice'),
    # 動画関連エンドポイント（一時的にコメントアウト）
    # path('videos/upload/', views.upload_video, name='upload_video'),
    # path('videos/analyze/', views.analyze_video, name='analyze_video'),
] 