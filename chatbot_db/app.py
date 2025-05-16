from flask import Flask, request, jsonify
import requests
import mysql.connector
import os

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data["user_input"]
    user_id = data["user_id"]
    session_id = data["session_id"]

    # 🔁 Send to chatbot API
    chatbot_url = "https://chatbot-q6k0.onrender.com/chat"
    chatbot_response = requests.post(chatbot_url, json={"message": user_input})
    ai_response = chatbot_response.json().get("response", "Sorry, no response.")

    # 🗃️ Save to DB
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO wp_ai_chatbot (user_id, session_id, user_input, ai_response) VALUES (%s, %s, %s, %s)",
        (user_id, session_id, user_input, ai_response)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "logged", "ai_response": ai_response})
