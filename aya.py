from urllib.request import urlopen
from bs4 import BeautifulSoup
from discord.ext import commands
import time
import discord
import asyncio

starttime = time.time()

desc = "Bunbunmaru arrives"
prefix = "?"




client = commands.Bot(command_prefix = prefix, description = desc)
@client.event
async def on_event(self):
	print('Logged in as')
	print(client.user.id)
	print('------')
	
@client.event
async def on_message(message):
	if message.content.startswith('Initalize Aya.exe'):
		while True:
			channel = client.get_channel('360042247770734593')
			wiki = "http://www.mynintendo.pl/"
			page = urlopen(wiki)
			soup = BeautifulSoup(page)

			title_help = soup.h2.string
			link = soup.find(title=title_help)
			if message.content != link:
				await client.send_message(channel, title_help)
				await client.send_message(channel, link.get("href"))
				message.content = link

			await asyncio.sleep(60)


client.run("Mzc5MDAyNDgwOTM3NDAyMzY4.DOjyhw.w0QsBBsIwAFxyW40odpZwUjs9ZY")