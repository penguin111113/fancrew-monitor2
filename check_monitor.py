import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.fancrew.jp/search/result/4"
LAST_FILE = "last_item.txt"

PUSHOVER_USER_KEY = "upjxy49vnsb3atpi7u2osjzg2u49uv"
PUSHOVER_API_TOKEN = "a747k4i85r9n9vrqtremrjezfog3t6"

def get_latest_item():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    item = soup.select_one('.monitorListItem')
    if not item:
        raise Exception("❌ monitorListItem が見つかりません。HTML構造が変わった可能性があります。")
    a_tag = item.select_one('a')
    title = a_tag.text.strip()
    link = "https://www.fancrew.jp" + a_tag['href']
    return title, link

def send_pushover_notification(title, link):
    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": "【新着】ファンくる通販モニター",
        "message": title,
        "url": link,
    }
    requests.post("https://api.pushover.net/1/messages.json", data=data)

def main():
    title, link = get_latest_item()
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            last_title = f.read().strip()
    else:
        last_title = ""

    if title != last_title:
        print("🔔 新着検出！通知送信中…")
        send_pushover_notification(title, link)
        with open(LAST_FILE, "w", encoding="utf-8") as f:
            f.write(title)
    else:
        print("📭 変更なし。通知なし。")

if __name__ == "__main__":
    main()
