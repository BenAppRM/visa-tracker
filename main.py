import requests
from bs4 import BeautifulSoup
import os

print("✅ visa-tracker script started")

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
URL = "https://it-ir-appointment.visametric.com/en"

try:
    # درخواست به سایت
    response = requests.get(URL, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # پیدا کردن تمام labelها و فیلتر کردن اونایی که شامل Study Visa هستن
    labels = soup.find_all("label")
    study_labels = [
        label.text.strip()
        for label in labels
        if "(CD)" in label.text or "Study Visa" in label.text
    ]

    if study_labels:
        message = "📘 Study Visa Options Found:\n\n" + "\n".join(study_labels)
        print("🎯 Found study visa labels:", study_labels)
    else:
        message = "⚠️ No Study Visa options found in current page."
        print("❌ No matching (CD) labels found.")

except Exception as e:
    message = f"❌ Error fetching data:\n{str(e)}"
    print("❌ Error:", e)

# ارسال پیام به تلگرام
try:
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    telegram_response = requests.post(telegram_url, data=payload, timeout=10)

    if telegram_response.ok:
        print("✅ Telegram message sent")
    else:
        print("⚠️ Telegram error:", telegram_response.text)

except Exception as e:
    print("❌ Failed to send Telegram message:", str(e))
