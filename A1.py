from flask import Flask
import threading
import time
import requests
from datetime import datetime

app = Flask(__name__)

# ================= CONFIG =================
A2_URL = "https://a2-xewy.onrender.com/ping"

OTHER_SERVICES = [
    "https://medilink-backend-24jm.onrender.com",
]
PING_INTERVAL = 4 * 60  # 4 minutes
# ==========================================


@app.route("/")
def home():
    return "A1 is running"


@app.route("/ping")
def ping():
    print_log("Received ping")
    return "pong from A1"


def print_log(message):
    print(f"[{datetime.now()}] A1 | {message}", flush=True)


def ping_services():
    while True:
        print_log("I am alive")

        # Ping A2
        try:
            requests.get(A2_URL, timeout=10)
            print_log("I called: A2")
        except Exception as e:
            print_log(f"A2 failed: {e}")

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

