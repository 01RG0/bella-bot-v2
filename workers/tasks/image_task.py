from ..worker import app

@app.task
def generate_image(prompt):
    # TODO: Implement image generation logic
    return f"Generated image for: {prompt}"