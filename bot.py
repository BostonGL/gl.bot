#GL Bot 2.0

#Discord
import discord
from discord import utils 
from discord.ext import commands
from discord.utils import get

#Cogs
from cogs import weather

#Other
from randomapi import RandomJSONRPC
import asyncio
import config
import requests
import wikipedia
import os
import sqlite3
import json

random_client = RandomJSONRPC(config.RANDOM)
wikipedia.set_lang("ru")
bot = commands.Bot(command_prefix='!')
client = discord.Client()
bot.remove_command('help')

@bot.event
async def on_ready():
	print("Bot is online")

@bot.event
async def on_member_join(member):
	#Добавление ролей
	roless = [692748791526457346, 692747803667202198, 692683592811282502, 692762692649353338, 702077659718484008, 692780034066481242]
	for x in range(1,len(roless)):
		role = discord.utils.get(member.guild.roles, id=roless[x])
		await member.add_roles(role)

	#Сообщение в лс
	print(f"[log] {member} зашел на сервер")
	await member.send('Добро пожаловать, Вы присоединились на сервер')
	await member.send('Не забудьте ознакомиться со следующими каналами, чтобы понять устройство сервера:')
	await member.send('#📕правила  – канал с правилами сервера')
	await member.send('#🔻система-ролей – канал с описанием ролей на сервере')
	await member.send('#🔺система-каналов – канал с описанием каналов на сервере')

@bot.event
async def on_raw_reaction_add(payload):
	message_id = payload.message_id
	if message_id == 692464837854232656:
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

		if payload.emoji.name == "cs":
			role = discord.utils.get(guild.roles, name="CS:GO")
		else:
			role = discord.utils.get(guild.roles, name=payload.emoji.name)

		if role is not None:
			member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
			if member is not None:
				await member.add_roles(role)
				print(f"[log] Роль {role} добавлена ползователю {member}")
			else:
				print('[log][error] Пользователь не найден')
		else:
			print('[log][error] Роль не найдена')
	elif message_id == 692680864022396980 and payload.emoji.name == "ok":
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
		role = discord.utils.get(guild.roles, name="Гражданин")
		member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
		await member.add_roles(role)
		role = discord.utils.get(member.guild.roles, id=702077659718484008)
		await member.remove_roles(role)
		print(f"[log] {member} согласился с правилами и присоединился к серверу")

@bot.event
async def on_raw_reaction_remove(payload):
	message_id = payload.message_id
	if message_id == 692464837854232656:
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

		if payload.emoji.name == "cs":
			role = discord.utils.get(guild.roles, name="CS:GO")
		else:
			role = discord.utils.get(guild.roles, name=payload.emoji.name)

		if role is not None:
			member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
			if member is not None:
				await member.remove_roles(role)
				print(f"[log] Роль {role} удалена у пользователя {member}")
			else:
				print('[log][error] Пользователь не найден')
		else:
			print('[log][error] Роль не найдена')


@bot.command()
async def weather(ctx, city):
	await ctx.send(weather.check_weather(city))

@bot.command()
async def rand(ctx, min, max):
	result = random_client.generate_integers(n=1, min=min, max=max).parse()

@bot.command()
async def ban(ctx, *, arg):
	num = random_client.generate_integers(n=1, min=1, max=10).parse()
	num = int(num[0])
	await ctx.send(config.RESPONSES[num])

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)
	print(f'[log] Удаляю {amount} сообщений')

@bot.command(aliases=['try'])
async def _try(ctx):
	rand = random_client.generate_integers(n=1, min=1, max=2).parse()
	rand = rand[0]
	a = ['', 'Успешно', 'Не успешно']
	await ctx.send(a[rand])

@bot.command()
async def wiki(ctx, *, args):
	result = wikipedia.page(args)
	await ctx.send(result.url)

@bot.command()
@commands.has_permissions(administrator = True)
async def cast_ban(ctx, member : discord.Member, *, reason = None):
	await ctx.send("omae wa mou shindeiru!")
	print(f'[log] {member} был забанен на этом сервере')
	await member.ban(reason = reason)

@bot.command()
@commands.has_permissions(ban_members=True)
async def Gulag(ctx, member : discord.Member):
	role = discord.utils.get(member.guild.roles, id=692699455727599676)
	await member.add_roles(role)
	await ctx.send(f"{member} был отправлен в гулаг")

@bot.command()
@commands.has_permissions(ban_members=True)
async def NoGulag(ctx, member : discord.Member):
	role = discord.utils.get(member.guild.roles, id=692699455727599676)
	await member.remove_roles(role)
	await ctx.send(f"{member} был освобожден из гулага")

@bot.command()
async def Mine(ctx):
	num = random_client.generate_integers(n=1, min=1, max=5).parse()
	num = int(num[0])
	num1 = random_client.generate_integers(n=1, min=1, max=10).parse()
	num1 = int(num1[0])
	responses = ["", "Алмазы", "Железо", "Камень", "Уголь", "Арбуз Ашота"]
	await ctx.send(f"Вы выкопали {responses[num]}. {num1} штук")

bot.run(config.TOKEN)
