import asyncio
import aiohttp
import os

from datetime import datetime
from dotenv import load_dotenv
from dateutil.parser import parse
from math import floor
from pytz import timezone

# from src.tasks.game_feed import game_feed

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.environ.get('SPORTS_RADAR_API_KEY')
VERSION = os.environ.get('SPORTS_RADAR_API_VERSION', 'v8')
ENV = os.environ.get('SPORTS_RADAR_API_ENV', 'trial')

headers = {'Content-Type': 'application/json'}

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
  async with aiohttp.ClientSession() as session:
      async with session.get(api_url, headers=headers) as response:
          # Get the response from the)
          if response.status >= 400:
             print('Server error found. Check Sports Radar api!')
             return
          schedule = await response.json()

          if schedule is None:
             return
          for game in schedule.get('games', []):
            if game.get('status') != 'scheduled':
                return
            
            # set a task to listen for game data
            now = datetime.now().astimezone(utc_timezone)
            game_date = parse(game['scheduled']).astimezone(utc_timezone)
            time_difference_seconds = floor((game_date - now).total_seconds())
            print(time_difference_seconds)
            # game_feed.apply_async((game['id'],), countdown=2)


async def job():
  await get_schedules()

if __name__ == '__main__':
   asyncio.run(job())