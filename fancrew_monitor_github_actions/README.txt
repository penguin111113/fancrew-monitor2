# Fancrew Monitor Notifier (GitHub Actions版)

このリポジトリは、https://www.fancrew.jp/search/result/4 に新着モニター案件が出たら
Pushover経由でスマホ通知を送るGitHub Actionsスクリプトです。

## 📦 ファイル構成

- `.github/workflows/monitor.yml` : 実行スケジュール設定 (15分おき)
- `check_monitor.py` : 本体スクリプト
- `requirements.txt` : 必要ライブラリ一覧

## 🚀 使い方

1. GitHubで新しいリポジトリを作成
2. このZIPを展開してアップロード
3. GitHubの右上 [⭐] ボタンの横 → `Actions` タブを開く
4. `monitor` ワークフローが登録されていることを確認
5. `Run workflow` で手動実行も可能！

## 🧪 備考

- Pushoverでの通知が受信されるには、事前にPushoverアプリをインストールし、User Key/API Tokenを設定しておく必要があります。
- 状態保存ファイル `last_item.txt` は GitHub Actions のワークスペース上に一時保存されます（リセットされる仕様です）