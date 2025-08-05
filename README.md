# 🏃‍♂️ Runners' Insight

ランニングフォーム解析・AIアドバイス生成システム

## 📖 プロジェクト概要

Runners' Insightは、ランニング動画を解析して個人に最適化されたアドバイスを提供するWebアプリケーションです。

### 主な機能

- **🎥 動画アップロード機能**: ランニング動画をアップロードして解析
- **📊 フォーム解析**: OpenCV・MediaPipeを使用した特徴量抽出
  - ピッチ（歩/分）
  - ストライド長（cm）
  - 着地角度（度）
  - 上下動（cm）
  - 接地時間（ms）
- **🤖 AIアドバイス生成**: 分析結果に基づくパーソナライズドアドバイス
- **📈 パフォーマンス向上支援**: 具体的な練習法とドリル提案

## 🛠 技術スタック

### フロントエンド
- **React** (TypeScript)
- **Vite** (開発サーバー)
- **CSS3** (モダンデザイン)

### バックエンド
- **Django** (Python)
- **Django REST Framework** (API)
- **SQLite** (開発環境)
- **Celery** (非同期処理)
- **Redis** (キャッシュ・メッセージブローカー)

### データ分析・AI
- **OpenCV** (動画解析)
- **MediaPipe** (ポーズ推定)
- **Pandas** (データ処理)
- **scikit-learn** (機械学習)

### デプロイ・インフラ
- **Docker** (コンテナ化)
- **Docker Compose** (オーケストレーション)
- **AWS EC2** (本番環境想定)

## 🚀 クイックスタート

### 前提条件
- Python 3.9+
- Node.js 18+
- npm または yarn

### ローカル開発環境のセットアップ

1. **リポジトリのクローン**
```bash
git clone https://github.com/YOUR_USERNAME/runners-insight.git
cd runners-insight
```

2. **バックエンドの起動**
```bash
cd backend
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver 127.0.0.1:8000
```

3. **フロントエンドの起動**
```bash
cd frontend
npm install
npm run dev
```

4. **ブラウザでアクセス**
- フロントエンド: http://localhost:5174/
- バックエンドAPI: http://127.0.0.1:8000/api/

## 📱 使用方法

### 基本的なワークフロー

1. **システム状態確認**: API接続状況をチェック
2. **モック分析実行**: テストデータでシステム動作を確認
3. **アドバイス生成**: 分析結果に基づく改善提案を取得

### 動画アップロード（今後実装予定）

1. ランニング動画をアップロード
2. 自動的にフォーム解析を実行
3. AI生成アドバイスを確認
4. 練習法とドリルを実践

## 🏗 プロジェクト構造

```
runners-insight/
├── backend/                 # Django バックエンド
│   ├── api/                # REST API エンドポイント
│   ├── apps/               # Django アプリケーション
│   │   ├── users/         # ユーザー管理
│   │   ├── videos/        # 動画管理
│   │   ├── analysis/      # 解析機能
│   │   └── advice/        # アドバイス生成
│   └── runners_insight/   # プロジェクト設定
├── frontend/               # React フロントエンド
│   ├── src/               # ソースコード
│   ├── public/            # 静的ファイル
│   └── dist/              # ビルド出力
├── data/                  # 分析用データ
├── docker-compose.yml     # Docker設定
└── README.md             # このファイル
```

## 📊 開発ステータス

- ✅ **基本システム構成**: 完了
- ✅ **フロントエンド UI**: 完了
- ✅ **バックエンド API**: 完了
- ✅ **モック分析・アドバイス**: 完了
- 🔄 **動画アップロード機能**: 開発中
- 🔄 **リアルタイム動画解析**: 開発中
- 📋 **データベース本格運用**: 予定
- 📋 **本番環境デプロイ**: 予定

## 🤝 コントリビューション

プロジェクトへの貢献を歓迎します！

1. フォークを作成
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチをプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は `LICENSE` ファイルを参照してください。

## 👥 作成者

- **開発者**: [あなたの名前]
- **プロジェクト**: Runners' Insight
- **作成日**: 2025年1月

## 🔗 関連リンク

- [プロジェクト進捗](./project_progress.md)
- [API ドキュメント](http://127.0.0.1:8000/api/)
- [技術仕様書](#) (今後追加予定)

---

**Runners' Insight** - ランニングパフォーマンス向上のためのスマートな解析システム 🏃‍♂️✨ 