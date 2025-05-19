# main.py (Playwright version)
import asyncio
from playwright.async_api import async_playwright
import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
URL = "https://it-ir-appointment.visametric.com/en"

async def run():
    print("✅ visa-tracker script started (Playwright)")

    message = ""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(URL, timeout=60000)

            # صبر می‌کنیم تا گزینه‌های Study Visa لود بشن
            await page.click("text=Study Visa")
            await page.wait_for_selector(".consularStudyVisaCD", timeout=5000)

            labels = await page.locator(".consularStudyVisaCD label").all_text_contents()
            if labels:
                message = "📘 Study Visa Options Found:\n\n" + "\n".join(labels)
                print("🎯 Extracted:", labels)
            else:
                message = "⚠️ No Study Visa options found."

            await browser.close()

    except Exception as e:
        message = f"❌ Playwright Exception:\n{str(e)}"
        print(message)

    # ارسال به تلگرام
    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        tg = requests.post(telegram_url, data=payload, timeout=10)
        if tg.ok:
            print("✅ Telegram message sent successfully.")
        else:
            print("⚠️ Telegram Error:", tg.text)
    except Exception as e:
        print("❌ Telegram send failed:", str(e))

if __name__ == "__main__":
    asyncio.run(run())
