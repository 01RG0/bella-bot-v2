from ..worker import app

@app.task
def generate_ai_response(message):
    # TODO: Implement AI response generation
    return f"AI response: {message}"