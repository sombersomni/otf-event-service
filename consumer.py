import redis
import time

r = redis.Redis(host='localhost', port=6379)
last_id =  b'1678310516474-0'
stream_key = "world"
sleep_ms = 5000

while True:
    try:
        time.sleep(2)
        resp = r.xread(
            {stream_key: last_id}, count=1, block=sleep_ms
        )
        if resp:
            key, messages = resp[0]
            last_id, data = messages[0]
            print("REDIS ID: ", last_id)
            print("      --> ", data)

    except ConnectionError as e:
        print("ERROR REDIS CONNECTION: {}".format(e))
