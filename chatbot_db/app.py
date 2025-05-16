from flask import Flask, request, jsonify
import mysql.connector
import os
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, origins=["https://staging4.bitcoiners.africa"])
# DB connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
    )

@app.route('/chat', methods=['POST'])
def log_chat():
    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    user_input = data.get('user_input')
    ai_response = data.get('ai_response')

    if not all([user_id, session_id, user_input, ai_response]):
        return jsonify({'status': 'error', 'message': 'Missing fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if session already exists
    cursor.execute("SELECT conversation_json FROM wp_ai_chatbot WHERE user_id=%s AND session_id=%s", (user_id, session_id))
    result = cursor.fetchone()

    if result:
        conversation_data = result[0] or {"conversation": []}
        if isinstance(conversation_data, str):
            conversation_data = json.loads(conversation_data)

        conversation_data["conversation"].append({
            "user": user_input,
            "ai": ai_response
        })

        cursor.execute(
            "UPDATE wp_ai_chatbot SET conversation_json=%s WHERE user_id=%s AND session_id=%s",
            (json.dumps(conversation_data), user_id, session_id)
        )
    else:
        conversation_data = {
            "conversation": [{
                "user": user_input,
                "ai": ai_response
            }]
        }

        cursor.execute(
            "INSERT INTO wp_ai_chatbot (user_id, session_id, conversation_json) VALUES (%s, %s, %s)",
            (user_id, session_id, json.dumps(conversation_data))
        )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "logged", "conversation": conversation_data})
