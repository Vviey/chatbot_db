from flask import Flask, request, jsonify
from interaction_logger import log_interaction
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    user_input = data.get('user_input')
    ai_response = data.get('ai_response')
    ai_response_links = data.get('ai_response_links')
    keywords = data.get('keywords')
    keyword_counts = data.get('keyword_counts')
    ip_address = request.remote_addr
    response_time = data.get('response_time')

    log_interaction(
        user_id=user_id,
        session_id=session_id,
        user_input=user_input,
        ai_response=ai_response,
        ai_response_links=ai_response_links,
        keywords=keywords,
        keyword_counts=keyword_counts,
        ip_address=ip_address,
        response_time=response_time
    )

    return jsonify({'status': 'logged'})
