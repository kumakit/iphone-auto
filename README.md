# iphone-auto (Mission Control - Plary Automation)

iPhone ミラーリングを介して、アプリの自動操作（プラリー等）を行うプロジェクトです。

## 使用方法
1. iPhone ミラーリングを起動し、「プラリー」アプリを開きます。
2. `uv run python src/main.py` を実行して、ウィンドウ認識とキャプチャをテストします。

## ディレクトリ構成
- `src/`: プログラムソースコード
- `images/`: テンプレート画像（認識用）
- `logs/`: 実行ログ、スクリーンショット
- `docs/`: 仕様・計画書

詳細は `docs/plan.md` を参照してください。
