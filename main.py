# main.py
import os
import requests
from bs4 import BeautifulSoup

# ==== 🟩 پیکربندی ====
SCRAPERAPI_KEY    = "61162cf2113cd4dffffa65f0ac310aad"
VISAMETRIC_URL    = "https://it-ir-appointment.visametric.com/en"
TELEGRAM_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID  = os.environ.get("TELEGRAM_CHAT_ID")

# ==== 🟦 توابع کمکی ====
def fetch_rendered_page(url: str) -> str:
    params = {
        "api_key": SCRAPERAPI_KEY,
        "url": url,
        "render": "true",       # رندر کامل JavaScript
        "country_code": "de",   # اختیاری: آلمان (نزدیک به سرور ایتالیا)
    }
    resp = requests.get("http://api.scraperapi.com", params=params, timeout=60)
    resp.raise_for_status()
    return resp.text

def extract_study_options(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find(id="consularStudyVisaCD")
    if not container:
        return []
    labels = container.find_all("label")
    return [lbl.get_text(strip=True) for lbl in labels if lbl.get_text(strip=True)]

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    r = requests.post(url, json=payload, timeout=10)
    if not r.ok:
        print("⚠️ Telegram error:", r.text)

# ==== ▶ اجرای اصلی ====
def main():
    try:
        html = fetch_rendered_page(VISAMETRIC_URL)
        options = extract_study_options(html)
        if options:
            text = "<b>Study Visa Options Found:</b>\n\n" + "\n".join(options)
        else:
            text = "⚠️ No Study Visa options found."
        send_telegram(text)
        print("✅ Done:", options or "none")
    except Exception as e:
        err = f"❌ Error: {e}"
        print(err)
        send_telegram(err)

if __name__ == "__main__":
    main()
