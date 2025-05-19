import asyncio
from playwright.async_api import async_playwright
import requests
import os

# ==== 🟩 پیکربندی ====
TELEGRAM_TOKEN = "8083030250:AAGrnBOMQ57l1HmWrGttl2jEy_ZpxUaLQX0"
TELEGRAM_CHAT_ID = "94785206"
BROWSERLESS_TOKEN = "2SLAotEtd7capyP5dbbd22885ef4f314250f80a78ff2354cf"

VISAMETRIC_URL = "https://it-ir-appointment.visametric.com/en"
CHECK_SELECTOR = "button:has-text('Study Visa')"  # یا هر دکمه‌ای که باید کلیک بشه

# ==== 🟦 تلگرام ====
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        print("✅ Telegram message sent successfully.")
    except Exception as e:
        print(f"⚠️ Telegram error: {e}")

# ==== 🟨 اجرای اصلی ====
async def run():
    print("✅ visa-tracker script started (Browserless.io)")

    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.connect(f"wss://chrome.browserless.io/playwright?token={BROWSERLESS_TOKEN}")
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(VISAMETRIC_URL, timeout=60000)
            await page.wait_for_selector(CHECK_SELECTOR, timeout=60000)
            await page.click(CHECK_SELECTOR)
            await page.screenshot(path="page.png", full_page=True)
            await page.wait_for_timeout(3000)
            send_telegram_message("🟢 Study Visa گزینه‌ای پیدا شد و کلیک شد!")
        except Exception as e:
            await page.screenshot(path="error.png", full_page=True)
            print(f"❌ Error fetching site:\n{e}")
            send_telegram_message("⚠️ No Study Visa options found or site blocked.")
        finally:
            await browser.close()
            await playwright.stop()

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        send_telegram_message(f"🚫 Script crashed: {e}")

# ==== ▶ اجرا ====
if __name__ == "__main__":
    asyncio.run(run())
