from urllib.request import urlopen
from bs4 import BeautifulSoup
from discord.ext import commands
import discord
import asyncio
import datetime


desc = "Bunbunmaru arrives"
prefix = "?"




client = commands.Bot(command_prefix = prefix, description = desc)
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.id)
	print('------')
	admin_channel = client.get_channel('255758512632627200')
	await client.send_message(admin_channel, 'Initalize Aya.exe')
	channel = client.get_channel('360042247770734593')
	now = datetime.datetime.now()
	log = client.logs_from(channel, limit=1, before=now)
	async for message in log:
		await client.send_message(admin_channel, message.content)
		help = message.content
	"""help = "tak"""
	while True:
		
		
		wiki = "http://www.mynintendo.pl/"
		page = urlopen(wiki)
		soup = BeautifulSoup(page)
		now = datetime.datetime.now()
		
		title_help = soup.h2.string
		link = soup.find(title=title_help).get("href")
		
			
		if help == link:
			await client.send_message(admin_channel, now)
		else:
			await client.send_message(channel, title_help)
			await client.send_message(channel, link)
			help = link
		await asyncio.sleep(60)


client.run("Mzc5MDAyNDgwOTM3NDAyMzY4.DOjyhw.w0QsBBsIwAFxyW40odpZwUjs9ZY")

