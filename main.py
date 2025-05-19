import requests
from bs4 import BeautifulSoup

# اطلاعات ربات و چت تلگرام
TELEGRAM_TOKEN = "8054642676:AAFsHDz1UKBfwBDKN5wfXU_Xys6Vhj4q3ro"
CHAT_ID = "94785206"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram error:", e)

def fetch_study_visa_options():
    url = "https://it-ir-appointment.visametric.com/en"
    try:
        response = requests.get(url, timeout=15)
    except Exception as e:
        send_telegram("⚠️ Error fetching the page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    section = soup.find("div", id="consularStudyVisaCD")
    if not section:
        send_telegram("❌ Study Visa section not found.")
        return []

    labels = section.find_all("label")
    return [label.get_text(strip=True) for label in labels]

def main():
    try:
        with open("old_options.txt", "r", encoding="utf-8") as f:
            old_options = f.read().splitlines()
    except FileNotFoundError:
        old_options = []

    current_options = fetch_study_visa_options()

    new_items = [opt for opt in current_options if opt not in old_options]
    if new_items:
        send_telegram("🆕 New Study Visa options found:\n" + "\n".join(new_items))

    with open("old_options.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(current_options))

if __name__ == "__main__":
    main()
