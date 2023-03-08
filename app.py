from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379)

@app.route('/publish', methods=['POST'])
def publish():
    data = request.get_json()
    event_name = data['event_name']
    message = data['message']
    print(event_name, message)
    r.xadd(event_name, {'message': message})
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
