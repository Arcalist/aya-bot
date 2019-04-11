from urllib.request import urlopen
from bs4 import BeautifulSoup
from discord.ext import commands
import discord
import asyncio
import os
import psycopg2

desc = "Bunbunmaru arrives"
prefix = "?"

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
cur.execute("SELECT * FROM token")
token = cur.fetchone()

pages = {"mynintendo": "https://www.mynintendo.pl/",
         "lowcyps4": "https://lowcygier.pl/platforma/ps4/",
         "lowcyswitch": "https://lowcygier.pl/platforma/nintendo-switch/",
         "lowcypc": "https://lowcygier.pl/platforma/pc/",
         "switch": "https://www.mynintendo.pl/category/nintendo-switch/",
         "3ds": "https://www.mynintendo.pl/category/wiadomosci/"}

client = commands.Bot(command_prefix=prefix, description=desc)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="Ayaya"))


async def check_pages():
    await client.wait_until_ready()
    while not client.is_closed:

        for category, page in pages.items():
            url = urlopen(page)
            soup = BeautifulSoup(url)
            link = soup.h2.a.get("href")
            if link == "https://lowcygier.pl/polecane/":
                link = soup.h2.find("a", {"class": "post-title-text"}).get("href")
            if "lowcy" in category:
                cur.execute("SELECT * FROM news where link = %s and platform = %s", (link, category))
            else:
                cur.execute("SELECT * FROM news where link = %s", (link,))
            # print(cur.fetchone())
            if cur.fetchone() is None:
                if "lowcy" in category:
                    if "ps4" in category:
                        cur.execute("SELECT channel FROM channels where category = %s", ('lowcyps4',))
                        for channel in cur.fetchall():
                            await client.send_message(client.get_channel(''.join(channel)), link)
                    elif "pc" in category:
                        cur.execute("SELECT channel FROM channels where category = %s", ('lowcypc',))
                        for channel in cur.fetchall():
                            await client.send_message(client.get_channel(''.join(channel)), link)
                    else:
                        cur.execute("SELECT channel FROM channels where category = %s", ('lowcyswitch',))
                        for channel in cur.fetchall():
                            await client.send_message(client.get_channel(''.join(channel)), link)

                else:
                    cur.execute("SELECT channel FROM channels where category = %s", ('mynintendo', ))
                    for channel in cur.fetchall():
                        await client.send_message(client.get_channel(''.join(channel)), link)

                cur.execute("UPDATE news SET link = %s WHERE platform = %s", (link, category))
                conn.commit()

            print(category, link)
        cur.execute("SELECT * FROM news")
        print(cur.fetchall())

        await asyncio.sleep(60)


@client.event
async def on_message(message):
    if message.channel.id == message.author.id:
        await client.send_message(message.channel, "Nie obsługuję privów")
    else:
        if message.content.startswith('aya track'):
            msg = message.content.lower().split()
            if len(msg) == 3 and msg[2] in ['lowcypc', 'lowcyswitch', 'lowcyps4', 'mynintendo']:
                cur.execute('INSERT INTO channels VALUES(%s, %s)', (str(message.channel.id), msg[2]))
                try:
                    conn.commit()
                    await client.send_message(message.channel, "Pomyślnie dodano do śledzenia (może)")
                except:
                    await client.send_message(message.channel, "Ayaya! Coś poszło nie tak")
            else:
                await client.send_message(message.channel, "Niestety nie mogę śledzić tej strony")
        if message.content.startswith('aya unsub'):
            cur.execute('DELETE FROM channels WHERE channel = (%s)', (str(message.channel.id),))
            conn.commit()
            await client.send_message(message.channel, "Pomyślnie usunięto kanał z powiadomień")

client.loop.create_task(check_pages())
client.run(''.join(token))
