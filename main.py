import requests
from bs4 import BeautifulSoup
import os

print("✅ visa-tracker script started")

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
URL = "https://it-ir-appointment.visametric.com/en"

if not BOT_TOKEN or not CHAT_ID:
    print("❌ Bot token or chat ID is missing!")
    exit()

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(URL, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # پیدا کردن همه گزینه‌های مربوط به Study Visa
    labels = soup.find_all("label")
    study_labels = [
        label.text.strip()
        for label in labels
        if "(CD)" in label.text
    ]

    if study_labels:
        message = "📘 Study Visa Options Found:\n\n" + "\n".join(study_labels)
        print("🎯 Extracted options:", study_labels)
    else:
        message = "⚠️ No Study Visa options found on the page."
        print("⚠️ No labels with (CD) found.")

except Exception as e:
    message = f"❌ Error while fetching or parsing:\n{str(e)}"
    print("❌ Exception:", e)

# ارسال پیام به تلگرام
try:
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    tg_response = requests.post(telegram_url, data=payload, timeout=10)

    if tg_response.ok:
        print("✅ Telegram message sent successfully.")
    else:
        print("⚠️ Telegram error:", tg_response.text)

except Exception as e:
    print("❌ Telegram exception:", str(e))
