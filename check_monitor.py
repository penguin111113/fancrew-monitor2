import requests
from bs4 import BeautifulSoup
import re
import os
from pushover import Client

URL = "https://www.fancrew.jp/search/result/4"

# Pushover 通知
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")

def send_notification(message):
    client = Client(PUSHOVER_USER_KEY, api_token=PUSHOVER_API_TOKEN)
    client.send_message(message, title="ファンクル モニター通知")

def get_monitor_count():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    count_text = soup.select_one('.monitorListWrap .total').text.strip()
    match = re.search(r'/\s*(\d+)', count_text)
    if not match:
        raise Exception("❌ 件数の取得に失敗しました。HTML構造が変わった可能性があります。")
    return int(match.group(1))

def load_last_count():
    try:
        with open('last_count.txt', 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return None

def save_last_count(count):
    with open('last_count.txt', 'w') as f:
        f.write(str(count))

def main():
    current_count = get_monitor_count()
    last_count = load_last_count()

    if last_count != current_count:
        message = f"🆕 モニター件数が変わりました！ {last_count or 'N/A'} → {current_count}件"
        send_notification(message)
        save_last_count(current_count)
    else:
        print("🔁 件数に変化なし")

if __name__ == "__main__":
    main()
