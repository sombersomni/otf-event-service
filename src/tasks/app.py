import os

from celery import Celery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672')

# Create a Celery instance
app = Celery('tasks', broker=BROKER_URL, include=['src.tasks.game_feed'])

# Configure Celery instance
app.config_from_object('src.tasks.config')

if __name__ == '__main__':
    app.start()