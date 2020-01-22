import requests
import json
from datetime import datetime
import feedparser
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

pages = {
         "mynintendo": "https://www.mynintendo.pl/feed/",
         "lowcyps4": "https://lowcygier.pl/platforma/ps4/feed/",
         "lowcyswitch": "https://lowcygier.pl/platforma/nintendo-switch/feed/",
         "lowcypc": "https://lowcygier.pl/platforma/pc/feed/"
        }

client = commands.Bot(command_prefix=prefix, description=desc)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="'aya help' for help"))


async def check_pages():
    await client.wait_until_ready()
    while not client.is_closed:
        for category, page in pages.items():
            try:
                news = feedparser.parse(page).entries[0]
                cur.execute("SELECT * FROM news where link = %s and platform = %s", (news.link, category))
                # print(cur.fetchone())
                if cur.fetchone() is None:
                    cur.execute("SELECT channel FROM channels where category = %s", (category, ))
                    for channel in cur.fetchall():
                        await client.send_message(client.get_channel(''.join(channel)), news.link)
                    cur.execute("UPDATE news SET link = %s WHERE platform = %s", (news.link, category))
                    conn.commit()
            except BaseException:
                pass
            
        await asyncio.sleep(60)


@client.event
async def on_message(message):
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
    if message.content == 'aya help':
        embed = discord.Embed(title="Szybka pomoc do Ayi", colour=discord.Colour(0x1))
        embed.add_field(name="aya help", value="Wyświetla tę komendę")
        embed.add_field(name="aya track 'platforma'", value="Dodaje obecny kanał do wysyłania wiadomości dotyczącej danej platformy\nMożliwe platformy:\nlowcyps4 - lowcygier.pl kategoria z promocjami dotyczące ps4\nlowcyswitch - lowcygier.pl kategoria z promocjami dotycące switcha\nlowcypc - lowcygier.pl kategoria z promocjami dotyczące\nmynintendo - newsy z mynintendo.pl\ngamehag")
        embed.add_field(name="aya unsub", value="Usuwa wszystkie śledzenia z tego kanału")

        await client.send_message(message.channel, embed=embed)


client.loop.create_task(check_pages())
client.run(''.join(token))


