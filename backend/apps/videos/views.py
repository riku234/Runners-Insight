import logging
import os
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Video

# ロガーを設定
logger = logging.getLogger(__name__)

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def upload_video(request):
    """
    動画ファイルアップロード処理
    アップロード完了後にCeleryタスクで解析を開始する
    """
    logger.info(f"[UPLOAD] Video upload request received from IP: {request.META.get('REMOTE_ADDR', 'unknown')}")
    
    try:
        # ファイルの存在確認
        if 'video' not in request.FILES:
            logger.warning("[UPLOAD] No video file provided in request")
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        video_file = request.FILES['video']
        logger.info(f"[UPLOAD] Processing video file: {video_file.name}, size: {video_file.size} bytes")
        
        # ファイル形式チェック
        allowed_types = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/webm']
        if video_file.content_type not in allowed_types:
            logger.warning(f"[UPLOAD] Unsupported video format: {video_file.content_type}")
            return Response({'error': 'Unsupported video format'}, status=status.HTTP_400_BAD_REQUEST)
        
        # ファイルサイズチェック (100MB制限)
        max_size = 100 * 1024 * 1024  # 100MB
        if video_file.size > max_size:
            logger.warning(f"[UPLOAD] File size too large: {video_file.size} bytes (max: {max_size})")
            return Response({'error': 'File size too large (max: 100MB)'}, status=status.HTTP_400_BAD_REQUEST)
        
        # ユーザー取得または作成（簡易実装）
        user, created = User.objects.get_or_create(
            username='default_user',
            defaults={'email': 'default@example.com'}
        )
        
        # ファイル名生成
        file_extension = os.path.splitext(video_file.name)[1]
        unique_filename = f"video_{uuid.uuid4().hex}{file_extension}"
        
        # Videoオブジェクト作成
        video_obj = Video.objects.create(
            user=user,
            video_file=video_file,
            title=request.data.get('title', video_file.name),
            description=request.data.get('description', ''),
            file_size=video_file.size,
            status='uploading'
        )
        
        logger.info(f"[UPLOAD] Video object created with ID: {video_obj.id}")
        
        # ファイル保存完了、ステータス更新
        video_obj.status = 'uploaded'
        video_obj.save()
        
        logger.info(f"[UPLOAD] Video file saved successfully. Video ID: {video_obj.id}")
        
        # --- Celeryタスク呼び出し（Celeryが利用できない場合はスキップ） ---
        logger.info(f"[CELERY TRIGGER] Preparing to start analysis task for video ID: {video_obj.id}")
        try:
            from apps.analysis.tasks import start_video_analysis_task
            logger.info(f"[CELERY TRIGGER] Calling start_video_analysis_task for video ID: {video_obj.id}")
            task_result = start_video_analysis_task.delay(video_obj.id)
            logger.info(f"[CELERY TRIGGER] Queued. Task ID: {task_result.id}, Video ID: {video_obj.id}")
            video_obj.status = 'processing'
            video_obj.save()
        except Exception as e:
            logger.warning(f"[CELERY TRIGGER] Celery not available or failed to start analysis task for video ID {video_obj.id}: {e}")
            # ローカル環境ではCeleryがないため、ステータスを'uploaded'のまま保持
            video_obj.status = 'uploaded'
            video_obj.save()
        
        # 成功レスポンス
        response_data = {
            'video_id': video_obj.id,
            'filename': video_file.name,
            'size': video_file.size,
            'content_type': video_file.content_type,
            'uploaded_at': video_obj.uploaded_at.isoformat(),
            'status': video_obj.status,
            'task_id': getattr(locals().get('task_result'), 'id', None)
        }
        
        logger.info(f"[UPLOAD] Upload process completed successfully for video ID: {video_obj.id}")
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"[UPLOAD] Unexpected error during video upload: {str(e)}", exc_info=True)
        return Response({'error': f'Failed to upload video: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_video_status(request, video_id):
    """
    動画処理ステータス確認
    """
    try:
        video = Video.objects.get(id=video_id)
        logger.info(f"[STATUS CHECK] Video ID: {video_id}, Status: {video.status}")
        
        return Response({
            'video_id': video.id,
            'status': video.status,
            'uploaded_at': video.uploaded_at.isoformat(),
            'processed_at': video.processed_at.isoformat() if video.processed_at else None,
            'title': video.title,
            'file_size': video.file_size
        })
        
    except Video.DoesNotExist:
        logger.warning(f"[STATUS CHECK] Video not found: {video_id}")
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"[STATUS CHECK] Error checking video status: {str(e)}")
        return Response({'error': 'Failed to check status'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
