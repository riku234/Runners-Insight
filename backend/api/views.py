from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
import os
import uuid

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """API健康チェック"""
    return Response({
        'status': 'OK',
        'message': 'Runners Insight API is running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_users(request):
    """ユーザー一覧取得（テスト用）"""
    users = User.objects.all()
    user_data = []
    for user in users:
        user_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined.isoformat(),
        })
    return Response({
        'users': user_data,
        'count': len(user_data)
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """ユーザー作成（テスト用）"""
    try:
        username = request.data.get('username')
        email = request.data.get('email', '')
        password = request.data.get('password', 'defaultpass123')
        
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined.isoformat(),
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': f'Failed to create user: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def upload_video(request):
    """動画ファイルアップロード"""
    try:
        if 'video' not in request.FILES:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        video_file = request.FILES['video']
        
        # ファイル形式チェック
        allowed_types = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/webm']
        if video_file.content_type not in allowed_types:
            return Response({'error': 'Unsupported video format'}, status=status.HTTP_400_BAD_REQUEST)
        
        # ファイルサイズチェック (100MB制限)
        if video_file.size > 100 * 1024 * 1024:
            return Response({'error': 'File size too large (max: 100MB)'}, status=status.HTTP_400_BAD_REQUEST)
        
        # ファイル名生成
        file_extension = os.path.splitext(video_file.name)[1]
        unique_filename = f"video_{uuid.uuid4().hex}{file_extension}"
        
        # ファイル保存
        file_path = default_storage.save(
            f"uploads/videos/{unique_filename}",
            ContentFile(video_file.read())
        )
        
        return Response({
            'video_id': unique_filename.replace(file_extension, ''),
            'filename': video_file.name,
            'size': video_file.size,
            'content_type': video_file.content_type,
            'uploaded_at': datetime.now().isoformat(),
            'file_path': file_path,
            'status': 'uploaded'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': f'Failed to upload video: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_video(request):
    """実際の動画解析（現在はモック実装）"""
    try:
        video_id = request.data.get('video_id')
        if not video_id:
            return Response({'error': 'video_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 現在はモックデータを返す（将来的にOpenCV/MediaPipeで実装）
        mock_analysis = {
            'analysis_id': f'analysis_{uuid.uuid4().hex[:8]}',
            'video_id': video_id,
            'analysis_timestamp': datetime.now().isoformat(),
            'features': {
                'cadence': 180.2,
                'stride_length': 127.8,
                'landing_angle': 11.5,
                'vertical_oscillation': 8.9,
                'ground_contact_time': 275.3
            },
            'analysis_confidence': 0.89,
            'status': 'completed',
            'processing_time_seconds': 15.7
        }
        
        return Response(mock_analysis, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': f'Failed to analyze video: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def mock_video_analysis(request):
    """モック動画解析結果"""
    mock_data = {
        'video_id': 'mock_video_001',
        'analysis_timestamp': datetime.now().isoformat(),
        'features': {
            'cadence': 182.5,
            'stride_length': 125.3,
            'landing_angle': 12.8,
            'vertical_oscillation': 9.2,
            'ground_contact_time': 285.6
        },
        'analysis_confidence': 0.87,
        'status': 'completed'
    }
    
    return Response(mock_data)

@api_view(['POST'])
@permission_classes([AllowAny])
def mock_generate_advice(request):
    """モックアドバイス生成"""
    try:
        data = request.data
        features = data.get('features', {})
        
        cadence = features.get('cadence', 182.5)
        stride_length = features.get('stride_length', 125.3)
        landing_angle = features.get('landing_angle', 12.8)
        vertical_oscillation = features.get('vertical_oscillation', 9.2)
        ground_contact_time = features.get('ground_contact_time', 285.6)
        
        advice_text = f"""
## 現状分析
あなたのランニングフォームを分析した結果、以下の特徴が確認されました：

### 主な計測データ
- **ピッチ**: {cadence}歩/分（目安: 180歩/分前後）
- **ストライド長**: {stride_length}cm
- **着地角度**: {landing_angle}度
- **上下動**: {vertical_oscillation}cm（目安: 8-12cm）
- **接地時間**: {ground_contact_time}ms（目安: 250ms以下）

## 優先改善点

### 1. ピッチの最適化
現在のピッチが{cadence}歩/分と、理想的な180歩/分に近い値です。継続して維持しましょう。

### 2. 接地時間の短縮
接地時間が{ground_contact_time}msとやや長めです。より効率的な走りのために短縮を目指しましょう。

## 具体的練習法

### ピッチ向上ドリル
1. **メトロノーム練習**: 180BPMに合わせて走る
2. **ショートステップ走**: 歩幅を狭めてピッチを上げる練習

### 接地時間短縮練習
1. **かかと上げ走**: 足裏全体での着地を意識
2. **バウンディング**: 地面からの素早い離脱を練習

## 期待効果
- ランニング効率の向上
- 怪我リスクの軽減
- 長距離でのパフォーマンス向上

## 注意点
急激な変更は避け、2-3週間かけて徐々に改善していきましょう。
        """
        
        mock_advice = {
            'advice_id': 'advice_001',
            'generated_at': datetime.now().isoformat(),
            'user_features': features,
            'advice_text': advice_text.strip(),
            'relevant_keywords': ['ピッチ', '接地時間', 'フォーム'],
            'confidence_score': 0.85,
            'llm_model': 'mock-gpt-3.5-turbo'
        }
        
        return Response(mock_advice, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': f'Failed to generate advice: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
