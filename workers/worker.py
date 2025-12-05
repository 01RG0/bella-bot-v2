from celery import Celery
import os

app = Celery('bella_worker', broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'))

@app.task
def process_ai_task(message):
    # TODO: Process AI task
    return f"Processed: {message}"

@app.task
def process_image_task(prompt):
    # TODO: Generate image
    return "Image URL"

if __name__ == '__main__':
    app.start()