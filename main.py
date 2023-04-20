import json
import os
from datetime import datetime

import timeago
from bottle import get, post, request, run, template

SMS_LEN_CAP = 50
SMS_PATH = os.path.join(os.path.dirname(__file__), "sms.json")
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")

def load_sms():
    try:
        with open(SMS_PATH, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        pass

    return []

def dump_sms(sms):
    with open(SMS_PATH, "w", encoding="utf-8") as f:
        json.dump(sms, f)

def readable_datetime(epoch):
    now = datetime.now()
    dt = datetime.fromtimestamp(epoch)
    return timeago.format(dt, now)

@get("/")
def get_index():
    return template("""<head>
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
    </head>
    <body style="height: 0%">
        <h1>SMS Server</h1>
        <p class="notice">Number: {{ number }}</p>
        %if sms:
            <table>
                <tr>
                    <th>From</th>
                    <th>Text</th>
                    <th>Time</th>
                </tr>
                %for msg in sms:
                <tr>
                    <td>{{ msg["from"] }}</td>
                    <td>{{ msg["text"] }}</td>
                    <td>{{ readable_datetime(msg["time"]) }}</td>
                </tr>
                %end
            </table>
        %else:
            <p class="notice">No messages yet.<p>
        %end
    </body>""",
    number=settings["number"],
    sms=load_sms(),
    readable_datetime=readable_datetime)

@post("/")
def post_index():
    msg = {}
    msg["from"] = request.json["from"]
    msg["text"] = request.json["text"]
    msg["time"] = request.json["receivedStamp"] / 1000

    sms = load_sms()
    sms.insert(0, msg)
    sms.sort(key=lambda d: d["time"], reverse=True)
    if len(sms) > SMS_LEN_CAP:
        sms = sms[:SMS_LEN_CAP]
    dump_sms(sms)

if __name__ == "__main__":
    with open(SETTINGS_PATH, encoding="utf-8") as f:
        settings = json.load(f)
        assert "port" in settings and isinstance(settings["port"], int)
        assert "number" in settings
    run(host="0.0.0.0", port=settings["port"])
