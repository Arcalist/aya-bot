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
 "lowcypc":"https://lowcygier.pl/platforma/pc/",
 "switch":"https://www.mynintendo.pl/category/nintendo-switch/",
 "3ds":"https://www.mynintendo.pl/category/wiadomosci/"}


client = commands.Bot(command_prefix = prefix, description = desc)
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.id)
	print('------')
	
	admin_channel = client.get_channel('255758512632627200')
	await client.send_message(admin_channel, 'Initalize Aya.exe')
	channel = client.get_channel('360042247770734593')
	lowcy_pc, lowcy_switch, lowcy_ps4 = client.get_channel('373841364053655573'), client.get_channel('477817276368683021'), client.get_channel('477817309067739157')
	while True:
			
		for category, page in pages.items():
			url = urlopen(page)
			soup = BeautifulSoup(url)
			link = soup.h2.a.get("href")
			if "lowcy" in category:
				cur.execute("SELECT * FROM news where link = %s and platform = %s", (link,category))   
			else:
				cur.execute("SELECT * FROM news where link = %s", (link,)) 
			#print(cur.fetchone())
			if cur.fetchone() is None:
				if "lowcy" in category:
					if link == "https://lowcygier.pl/polecane/":
						link = soup.h2.find("a", {"class": "post-title-text"}).get("href")
					if "ps4" in category:
						await client.send_message(lowcy_ps4, link)
					elif "pc" in category:
						await client.send_message(lowcy_pc, link)
					else:
						await client.send_message(lowcy_switch, link)
					
				else:
					await client.send_message(channel, link)
				cur.execute("UPDATE news SET link = %s WHERE platform = %s",(link, category))
				conn.commit()  
				
			print(category,link)
		cur.execute("SELECT * FROM news")
		print(cur.fetchall())
		
			
		await asyncio.sleep(60)


client.run(''.join(token))

