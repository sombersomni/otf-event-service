import asyncio
import aiohttp
import os

from celery import Celery
from datetime import datetime, timedelta
from dotenv import load_dotenv
from dateutil.parser import parse
from math import floor
from pytz import timezone

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.environ.get('SPORTS_RADAR_API_KEY')
VERSION = os.environ.get('SPORTS_RADAR_API_VERSION', 'v8')
ENV = os.environ.get('SPORTS_RADAR_API_ENV', 'trial')

# Create a Celery instance
broker_url = 'amqp://guest:guest@localhost:5672'
app = Celery('tasks', broker=broker_url)

@app.task
def create_file(name: str):
  try:
    with open(f"{name}.txt", 'w') as file:
        # Open the file in write mode ('w') and automatically close it when done
        pass
    print(f"File '{name}' created successfully.")
  except Exception as e:
      print(f"An error occurred while creating the file: {str(e)}")

async def get_schedules():
  # Get Schedules for all games per day
  utc_timezone = timezone('UTC')
  now = datetime.now().astimezone(utc_timezone)
  year = now.year
  month = f"0{now.month}" if now.month < 10 else f"{now.month}"
  day = f"0{now.day}" if now.day < 10 else f"{now.day}"
  api_url = (
    f"https://api.sportradar.com/nba/{ENV}/{VERSION}/en/games/{year}/{month}/{day}/schedule.json"
    f"?api_key={API_KEY}"
  )
  print(api_url)
  async with aiohttp.ClientSession() as session:
      async with session.get(api_url) as response:
          # Get the response from the
          schedule = await response.json()
          print(schedule)
          if schedule is None:
             return
          for game in schedule.get('games', []):
            if game.get('status') != 'scheduled':
                return
            
            # set a task to listen for game data
            now = datetime.now().astimezone(utc_timezone)
            game_date = parse(game['scheduled']).astimezone(utc_timezone)
            time_difference_seconds = floor((game_date - now).total_seconds())
            time_difference_seconds
            app.send_task('tasks.create_file', (game['id'],), countdown=2)




async def job():
  await get_schedules()

if __name__ == '__main__':
   asyncio.run(job())