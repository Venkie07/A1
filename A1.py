from flask import Flask
import threading
import time
import requests
from datetime import datetime

app = Flask(__name__)

# ================= CONFIG =================
ALIAS2_URL = "https://alias2.onrender.com/ping"

OTHER_SERVICES = [
    "https://medilink-backend-24jm.onrender.com",
]
PING_INTERVAL = 4 * 60  # 4 minutes
# ==========================================


@app.route("/")
def home():
    return "Alias1 is running"


@app.route("/ping")
def ping():
    print_log("Received ping")
    return "pong from alias1"


def print_log(message):
    print(f"[{datetime.now()}] alias1 | {message}", flush=True)


def ping_services():
    while True:
        print_log("I am alive")

        # Ping alias2
        try:
            requests.get(ALIAS2_URL, timeout=10)
            print_log("I called: alias2")
        except Exception as e:
            print_log(f"alias2 failed: {e}")

        # Ping other services
        for url in OTHER_SERVICES:
            try:
                requests.get(url, timeout=10)
                print_log(f"I called: {url}")
            except Exception as e:
                print_log(f"{url} failed: {e}")

        time.sleep(PING_INTERVAL)


if __name__ == "__main__":
    threading.Thread(target=ping_services, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
