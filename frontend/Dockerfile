# ビルドステージ
FROM node:18-alpine AS builder

WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm ci

# ソースコードをコピー
COPY . .

# Reactアプリをビルド
RUN npm run build

# プロダクションステージ
FROM nginx:alpine

# カスタムnginx設定をコピー
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# ビルドされたファイルをnginxの公開ディレクトリにコピー
COPY --from=builder /app/dist /usr/share/nginx/html

# ポートを公開
EXPOSE 80

# nginxを起動
CMD ["nginx", "-g", "daemon off;"]
