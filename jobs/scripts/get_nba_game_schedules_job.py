import asyncio
import aiohttp
import os
import load_env

url = "https://api.sportradar.com/nba/simulation/v7/en/games/a2a43125-5538-43f7-84a9-e8e02a8a772f/pbp.json"
async def job():
  api_url = (
    "https://api.sportradar.com/nba/simulation/v7/en/games/a2a43125-5538-43f7-84a9-e8e02a8a772f/pbp.json"
    + f"?api_key={os.environ.get('SPORTS_RADAR_API_KEY')}"
  )
  async with aiohttp.ClientSession() as session:
      async with session.get(api_url) as response:
          # Get the response from the 
          print('get data')
          data = await response.json()
          print()

if __name__ == '__main__':
   asyncio.run(job)