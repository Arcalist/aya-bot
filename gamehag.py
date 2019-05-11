import requests
import json
import time
response = requests.get('https://gamehag.com/api/v2/news?token=zMoIilzTXnAXXXX')
response.encoding = 'utf-8'
data = response.json()
article = data['collection'][0]
cur.execute("SELECT * FROM gamehag WHERE timestamp = %s", (article['created_at'], ))

if cur.fetchone is None:
    cur.execute("Select * FROM gamehag ORDER BY timestamp DESC limit 1")
    most_recent = cur.fetchone()

    f = "%Y-%m-%d %H:%M:%S"
    t_stamp = time.strptime(article['created_at'], f)
    most_recent_stamp = time.strptime(''.join(most_recent), f)

    if t_stamp > most_recent_stamp:
        cur.execute("INSERT INTO gamehag VALUES(%s)", article['created_at'])
        conn.commit()
        await client.send_message(client.get_channel('255758512632627200'), 'https://gamehag.com/pl/artykuly/'+s['url'])


