from urllib.request import urlopen
from bs4 import BeautifulSoup
from discord.ext import commands
import discord
import asyncio
import os
import psycopg2

desc = "Bunbunmaru arrives"
prefix = "?"

conn = psycopg2.connect(dbname = "db3qhkvtsi2nu", user = "qyinrlseznzfru", password="e090d984a640d447a4d6eb0d61cd488da690c9f4fc3d34346ff3ce4ef64fe5be", host = "ec2-54-217-250-0.eu-west-1.compute.amazonaws.com", port = 5432, sslmode='require')
cur = conn.cursor()

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

			cur.execute("SELECT * FROM news where link = %s", (link,))   
			#print(cur.fetchone())
			if cur.fetchone() is None:
				if "lowcy" in category:
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


client.run("Mzc5MDAyNDgwOTM3NDAyMzY4.DOjyhw.w0QsBBsIwAFxyW40odpZwUjs9ZY")

