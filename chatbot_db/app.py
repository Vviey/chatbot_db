from flask import Flask, request, jsonify
import mysql.connector
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://staging4.bitcoiners.africa", "https://bitcoiners.africa"])

#STAGING
def get_db1_connection():
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
    )

#LIVE
def get_db2_connection():
    return mysql.connector.connect(
        host=os.environ['DB2_HOST'],
        user=os.environ['DB2_USER'],
        password=os.environ['DB2_PASSWORD'],
        database=os.environ['DB2_NAME']
    )


@app.route('/')
def index():
    return "Chatbot API is running!"

@app.route('/chat', methods=['POST'])
def log_chat():
    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    user_input = data.get('user_input')
    ai_response = data.get('ai_response')
    ai_response_links = data.get('ai_response_links')  # optional
    keywords = data.get('keywords')  # optional
    keyword_counts = data.get('keyword_counts')  # optional, should be JSON/dict

    if not all([user_id, session_id, user_input, ai_response]):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert each chat interaction as a new row
    sql = """
    INSERT INTO wp_ai_chatbot
    (user_id, session_id, user_input, ai_response, ai_response_links, keywords, keyword_counts)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Convert keyword_counts dict to JSON string if provided
    keyword_counts_json = None
    if keyword_counts:
        import json
        keyword_counts_json = json.dumps(keyword_counts)

    cursor.execute(sql, (
        user_id,
        session_id,
        user_input,
        ai_response,
        ai_response_links,
        keywords,
        keyword_counts_json
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "logged"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
