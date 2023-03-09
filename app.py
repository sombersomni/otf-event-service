import aiohttp
from flask import Flask, jsonify, request
import redis
from datetime import datetime
import pytz

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379)

api_url = "https://api.sportradar.com/nba/simulation/v7/en/games/a2a43125-5538-43f7-84a9-e8e02a8a772f/pbp.json?api_key=zr4agcnkmbx9evcvt49xxat9"

@app.route('/publish', methods=['POST'])
def publish():
    data = request.get_json()
    event_name = data['event_name']
    message = data['message']
    print(event_name, message)
    r.xadd(event_name, {'message': message})
    return jsonify({'success': True})

@app.route('/', methods=['GET'])
async def index():
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            # Get the response from the 
            print('get data')
            data = await response.json()
            return jsonify(data)

# Set the time-to-live for the game score hash to one day (in seconds)
HASH_TTL = 86400
# Set the input date time string and the target timezone
game_scheduled_time_str = '2023-02-9T00:00:00+00:00'
target_tz = 'US/Eastern'
status = "open"

@app.route('/game_score', methods=['POST'])
def update_game_score():
    # Convert the input string to a datetime object
    game_scheduled_time = datetime.fromisoformat(game_scheduled_time_str)

    # Set the timezone of the datetime object to UTC
    game_scheduled_time_utc = game_scheduled_time.astimezone(pytz.utc)

    # Set the timezone of the datetime object to the target timezone
    target_tz_obj = pytz.timezone(target_tz)
    game_scheduled_time_est = game_scheduled_time_utc.astimezone(target_tz_obj)

    # Get the current datetime in the target timezone
    current_date_time_est = datetime.now(target_tz_obj)

    # Compare the two datetimes
    if status == 'closed':
        print('stop polling for this game id')
        return jsonify({ "skip": True })
    if current_date_time_est < game_scheduled_time_est:
        print('set the polling time out based on the difference in time')
        diff_time = current_date_time_est - game_scheduled_time_est
        return jsonify({ "cronjob_time": diff_time})

    print('game is likely running')

    # Retrieve the current game score and request count from Redis
    game_data = r.hgetall('game_score')
    print(game_data)
    current_score = int(game_data.get(b'score', b'0'))
    request_count = int(game_data.get(b'count', b'0'))

    # Get the new score from the request data
    new_score = request.json.get('score')
    print(current_score, new_score)
    # Add the new score to the current score and increment the request count
    updated_score = current_score + new_score
    updated_count = request_count + 1

    # Save the updated score and count back to Redis
    r.hmset('game_score', {'score': updated_score, 'count': updated_count})

    # Set the time-to-live for the game score hash
    r.expire('game_score', HASH_TTL)

    # Return the updated score and count to the user
    return jsonify({'score': updated_score, 'count': updated_count})

if __name__ == '__main__':
    app.run()
