from db_connection import get_connection

def log_interaction(user_id, session_id, user_input, ai_response, ai_response_links=None,
                    keywords=None, keyword_counts=None, ip_address=None, response_time=None):
    query = """
        INSERT INTO wp_ai_chatbot (
            user_id, session_id, user_input, ai_response, ai_response_links,
            keywords, keyword_counts, ip_address, response_time
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        user_id, session_id, user_input, ai_response, ai_response_links,
        keywords, keyword_counts, ip_address, response_time
    )

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, values)
        conn.commit()
    finally:
        conn.close()
