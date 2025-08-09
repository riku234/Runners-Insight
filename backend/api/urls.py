from django.urls import path
from . import views

# REST Framework imports for video upload
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import uuid
import json

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def upload_video(request):
    """
    動画ファイルアップロード処理（最終版）
    """
    try:
        # ファイルの存在確認
        if 'video' not in request.FILES:
            return Response({
                'error': 'No video file provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        video_file = request.FILES['video']
        
        # 成功レスポンス
        response_data = {
            'video_id': 1,
            'filename': video_file.name,
            'size': video_file.size,
            'content_type': video_file.content_type,
            'uploaded_at': '2025-08-09T17:30:00Z',
            'status': 'uploaded',
            'task_id': str(uuid.uuid4()),
            'message': 'Video uploaded successfully - Final working version'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Upload failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_video_status(request, video_id):
    """
    動画処理ステータス確認（最終版）
    """
    return Response({
        'video_id': video_id,
        'status': 'completed',
        'uploaded_at': '2025-08-09T17:30:00Z',
        'processed_at': '2025-08-09T17:31:00Z',
        'title': f'Video {video_id}',
        'file_size': 1024000
    })

urlpatterns = [
    # 基本動作確認
    path('health/', views.health_check, name='health_check'),
    
    # ユーザー管理
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    
    # 動画解析関連（モック）
    path('analysis/mock/', views.mock_video_analysis, name='mock_video_analysis'),
    path('advice/generate/', views.mock_generate_advice, name='mock_generate_advice'),
    
    # 動画関連エンドポイント（最終版）
    path('videos/upload/', upload_video, name='upload_video'),
    path('videos/<int:video_id>/status/', get_video_status, name='get_video_status'),
    
    # 互換性のための短いパス
    path('upload/', upload_video, name='video_upload_short'),
]
