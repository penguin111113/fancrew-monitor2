import requests
from bs4 import BeautifulSoup
import json
import os

# 設定
URL = "https://www.fancrew.jp/search/result/4"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
LAST_ITEMS_FILE = "last_items.json"
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def fetch_current_items():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select(".monitorListItem h3")
    titles = [item.text.strip() for item in items]
    print(f"✅ 現在のモニター件数: {len(titles)}")
    return titles

def load_last_items():
    if not os.path.exists(LAST_ITEMS_FILE):
        return []
    with open(LAST_ITEMS_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)

def save_last_items(items):
    with open(LAST_ITEMS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def send_slack_notification(message):
    if not SLACK_WEBHOOK_URL:
        print("⚠️ SLACK_WEBHOOK_URL が設定されていません")
        return

    payload = {"text": message}

    try:
        res = requests.post(SLACK_WEBHOOK_URL, json=payload)
        res.raise_for_status()
        print("📨 Slack通知を送信しました")
    except Exception as e:
        print("❌ Slack通知送信エラー:", e)

def main():
    current_items = fetch_current_items()
    last_items = load_last_items()

    added = list(set(current_items) - set(last_items))
    removed = list(set(last_items) - set(current_items))

    print(f"🆕 追加件数: {len(added)}")
    print(f"🗑️ 削除件数: {len(removed)}")

    if added or removed:
        message_lines = ["【ファンクル画像投稿モニターの変動通知】"]
        if added:
            message_lines.append(f"追加: {len(added)}件")
            for a in added:
                message_lines.append(f"＋ {a}")
        if removed:
            message_lines.append(f"削除: {len(removed)}件")
            for r in removed:
                message_lines.append(f"－ {r}")
        send_slack_notification("\n".join(message_lines))
        save_last_items(current_items)
    else:
        print("🔁 モニターの変化なし")

if __name__ == "__main__":
    main()
