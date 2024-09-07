from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime

app = Flask(__name__)

# Your Bot User OAuth Token
slack_token = "xoxb-your-token"
client = WebClient(token=slack_token)

@app.route('/')
def hello_world():
    current_datetime = datetime.now()
    f"Hello, World! The current date and time is: {current_datetime}"
    return "Hello, World! Shilpa"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # Handle the URL verification challenge from Slack
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    if "event" in data:
        event_type = data["event"]["type"]
        if event_type == "message" and not "bot_id" in data["event"]:
            channel_id = data["event"]["channel"]
            user = data["event"]["user"]
            text = data["event"]["text"]

            try:
                response = client.chat_postMessage(
                    channel=channel_id,
                    text=f"Hello <@{user}>! You said: {text}"
                )
            except SlackApiError as e:
                print(f"Error sending message: {e.response['error']}")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5001, debug = True)
