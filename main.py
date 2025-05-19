import requests
from bs4 import BeautifulSoup
import os
import asyncio
from playwright.async_api import async_playwright

print("✅ visa-tracker script started (Playwright)")

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
URL = "https://it-ir-appointment.visametric.com/en"

async def run():
    message = ""

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(URL, timeout=60000)

            await page.click("text=Study Visa")
            await page.wait_for_selector(".consularStudyVisaCD", timeout=5000)

            labels = await page.locator(".consularStudyVisaCD label").all_text_contents()
            if labels:
                message = "📘 Study Visa Options Found:\n\n" + "\n".join(labels)
                print("🎯 Extracted options:", labels)
            else:
                message = "⚠️ No Study Visa options found."

            await browser.close()

    except Exception as e:
        message = f"❌ Error fetching site:\n{str(e)}"
        print(message)

    # ارسال به تلگرام
    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        tg = requests.post(telegram_url, data=payload, timeout=10)

        if tg.ok:
            print("✅ Telegram message sent successfully.")
        else:
            print("⚠️ Telegram error:", tg.text)

    except Exception as e:
        print("❌ Telegram send failed:", str(e))

if __name__ == "__main__":
    asyncio.run(run())
