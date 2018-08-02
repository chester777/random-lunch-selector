from flask import Flask, render_template
import threading
from datetime import datetime
import time
import sqlite3

app = Flask(__name__)

dayFlag = None
dayResult = dict()

today = datetime.today()
todayTime = datetime(today.year, today.month, today.day)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/result', methods=["POST"])
def result():
    global dayResult
    global dayFlag

    if dayFlag is True:
        return render_template("finished.html", result = dayResult)

    elif dayFlag is False:
        conn = sqlite3.connect("store.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM store ORDER BY RANDOM() LIMIT 1")

        rows = cur.fetchall()

        for row in rows:
            dayResult["store_number"] = row[0]
            dayResult["store_name"] = row[1]
            dayResult["prefered_count"] = row[2]

            dayFlag = True

        return render_template("result.html", result = dayResult)

def day_check():
    global todayTime
    global dayFlag

    while True:
        currentTime = datetime.now()
        if (currentTime - todayTime).days > 0:
            todayTime = datetime(currentTime.year, currentTime.month, currentTime.day)
            dayFlag = False

        print(" * Check: the date has changed.")
        time.sleep(3600)

if __name__ == '__main__':

    dayFlag = False

    threadWeb = threading.Thread(target=app.run, args=("0.0.0.0",))
    threadDayCheck = threading.Thread(target=day_check)
    threadWeb.start()
    threadDayCheck.start()