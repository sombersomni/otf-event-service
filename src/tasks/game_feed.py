from src.tasks.app import app

@app.task
async def game_feed(game_id: str):
  return game_id
