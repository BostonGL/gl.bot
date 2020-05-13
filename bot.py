#GL Bot 2.0

#Discord
import discord
from discord import utils 
from discord.ext import commands
from discord.utils import get

#Other
import random
import asyncio
import config
import requests
import wikipedia
import os
import sqlite3
import json
import math
import pyowm
from PIL import Image, ImageFont, ImageDraw
import io

wikipedia.set_lang("ru")
bot = commands.Bot(command_prefix=config.PREFIX)
client = discord.Client()
bot.remove_command('help')
owm = pyowm.OWM('a5a9581344154c5c50433466c32affdd', language = "ru")

conn = sqlite3.connect("Discord.db")
cursor = conn.cursor()

#cursor.execute('''CREATE TABLE users (id int, balance real, lvl int, xp int)''')

@bot.event
async def on_ready():
	print("Bot is online")
	for guild in bot.guilds:
		print(guild)
		guild = guild
		for member in guild.members:
			cursor.execute(f"SELECT id FROM users where id={member.id}")
			if cursor.fetchone() == None:
				cursor.execute(f"INSERT INTO users VALUES ({member.id},100, 1, 0)")
			else:
				pass
			conn.commit()

@bot.event
async def on_member_join(member):
	cursor.execute(f"SELECT id FROM users where id={member.id}")
	if cursor.fetchone() == None:
		cursor.execute(f"INSERT INTO users VALUES ({member.id},100, 1, 0)")
	else:
		pass
	conn.commit()

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

@bot.event
async def on_command_error(ctx, error):
	print(error)
	if isinstance(error, commands.CommandOnCooldown):
		cd = int(error.retry_after)
		embed = discord.Embed(title = f'Команда находиться в кд. Повоторите через {cd}сек!', color=0xeb4132)
		await ctx.send(embed=embed)
	elif isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title = f':x: Недостаточно прав!', color=0xeb4132)


@bot.command()
async def rand(ctx, min : int, max : int):
	result = random.randint(min, max)
	await ctx.send(result)

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, arg):
	num = random.randint(0, len(config.RESPONSES))
	await ctx.send(config.RESPONSES[num])

@bot.command(aliases=['c'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
	amount = amount + 1
	await ctx.channel.purge(limit=amount)
	amount = amount - 1
	await ctx.send(embed = discord.Embed(description = f":white_check_mark: Удалено {amount} сообщений"))
	print(f'[log] Удаляю {amount} сообщений')

@bot.command()
async def wiki(ctx, *, args):
	result = wikipedia.page(args)
	await ctx.send(result.url)

@bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member : discord.Member, *, reason = None):
	print(f'[log] {member} был забанен на этом сервере')
	emb = discord.Embed(description = f":no_entry_sign: {member} был забанен на этом сервере.")
	ctx.send(embed = emb)	
	await member.ban(reason = reason)

@bot.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, member : discord.Member, *, reason = None):
	print(f"[log] {member} был кикнут с этого сервера")
	emb = discord.Embed(description = f":no_entry_sign: {member} был кикнут с этого сервера.")
	ctx.send(embed = emb)
	await member.kick(reason = reason)

@bot.command()
@commands.has_permissions(ban_members=True)
async def Ork(ctx, member : discord.Member):
	role = discord.utils.get(member.guild.roles, id=692699455727599676)
	await member.add_roles(role)
	await ctx.send(f"{member} стал оркам")

@bot.command()
@commands.has_permissions(ban_members=True)
async def UnOrk(ctx, member : discord.Member):
	role = discord.utils.get(member.guild.roles, id=692699455727599676)
	await member.remove_roles(role)
	await ctx.send(f"{member} больше не орк")

@bot.command(aliases=['mine'])
@commands.cooldown(1, 120, commands.BucketType.user)
async def Mine(ctx):
	price = None
	cursor.execute(f"SELECT lvl FROM users WHERE id={ctx.message.author.id}")
	lvl = cursor.fetchone()[0]
	cursor.execute(f"SELECT xp FROM users WHERE id={ctx.message.author.id}")
	exp = cursor.fetchone()[0]
	cursor.execute(f"SELECT balance FROM users WHERE id={ctx.message.author.id}")
	balance = cursor.fetchone()[0]

	num = random.randint(1, 100)
	if num < 30:
		response = "камень"
		xp = 1
		price = 2
	elif num > 30 and num < 55:
		response = "уголь"
		xp = 3
		price = 4
	elif num > 55 and num < 75:
		response = "железо"
		xp = 5
		price = 6
	elif num > 75 and num < 85:
		response = "золото"
		xp = 8
		price = 9
	elif num > 85 and num < 90:
		response = "алмаз"
		xp = 12
		price = 14
	elif num > 90 and num < 99:
		response = "серебро"
		xp = 7
		price = 8
	elif num == 100:
		response = "сундук с золотом"
		xp = 20
		price = 30

	price = price + lvl * 0.125 * price
	result = balance + price
	exp = exp + xp
	await ctx.send(embed = discord.Embed(title=f"Вы выкопали {response} и получили {price}GLC, {xp}xp"))
	cursor.execute(f"UPDATE users SET xp={exp} WHERE id={ctx.message.author.id}")
	cursor.execute(f"UPDATE users SET balance={result} WHERE id={ctx.message.author.id}")
	if exp >= 100 + lvl * 0.25 * 100:
		lvl = lvl + 1
		await ctx.send(f"Вы повысили уровень до {lvl}лвл")
		cursor.execute(f"UPDATE users SET lvl={lvl} WHERE id={ctx.message.author.id}")
	conn.commit()

@bot.command()
async def balance(ctx):
	cursor.execute(f"SELECT balance FROM users WHERE id={ctx.message.author.id}")
	content = cursor.fetchone()
	embed = discord.Embed(description = f"**Баланс пользователя {ctx.message.author} - {content[0]}GLC**")
	await ctx.send(embed = embed)

@bot.command()
async def pay(ctx, amount : float, member : discord.Member):
	cursor.execute(f"SELECT balance FROM users WHERE id={ctx.message.author.id}")
	author_balance = cursor.fetchone()[0]
	if amount > author_balance or amount < 0:
		embed = discord.Embed(description=f":x: На вашем счете недостаточно средств", color=0xeb4132)
		await ctx.send(embed = embed)
	elif amount < author_balance and amount > 0:
		cursor.execute(f"SELECT balance FROM users WHERE id={member.id}")
		member_balance = cursor.fetchone()[0]
		result = member_balance + amount
		result1 = author_balance - amount
		cursor.execute(f"UPDATE users SET balance={result} WHERE id={member.id}")
		cursor.execute(f"UPDATE users SET balance={result1} WHERE id={ctx.message.author.id}")
		embed = discord.Embed(description=f":white_check_mark: Транзакция прошла успешно. На счет {member} переведено {amount}GLC", color=0x2ecc71)
		await ctx.send(embed = embed)
		conn.commit()

@bot.command()
async def weather(ctx, place):
	observation = owm.weather_at_place(place)
	w = observation.get_weather()
	temp = w.get_temperature('celsius')["temp"]
	wind = w.get_wind()['speed']
	hum = w.get_humidity()  
	temp_max = w.get_temperature('celsius')['temp_max']
	temp_min = w.get_temperature('celsius')['temp_min']

	embed = discord.Embed(title = f"Прогноз погоды для города {place}")
	embed.description=(
		f":chart_with_upwards_trend: Макс.температура: **{temp_max}**\n\n"
		f":chart_with_downwards_trend: Мин.температура: **{temp_min}**\n\n"
		f":white_sun_rain_cloud: Погода: **{w.get_detailed_status()}**\n\n"
		f":dash: Ветер: **{wind}м/c**\n\n"
		f":droplet: Влажность: **{hum}**\n\n"
	)

	embed.set_thumbnail(url=ctx.guild.icon_url)
	await ctx.send(embed = embed)

@bot.command()
async def server(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"{ctx.guild.name}", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: Сервер создали: **{ctx.guild.created_at.strftime('%A, %b %#d %Y')}**\n\n"
        f":flag_white: Регион: **{ctx.guild.region}\n\nГлава сервера: **{ctx.guild.owner}**\n\n"
        f":tools: Ботов на сервере: **{len([m for m in members if m.bot])}**\n\n"
        f":green_circle: В сети: **{online}**\n\n"
        f":black_circle: Не в сети: **{offline}**\n\n"
        f":yellow_circle: Не активен: **{idle}**\n\n"
        f":red_circle: Не беспокоить: **{dnd}**\n\n"
        f":shield: Уровень верификации: **{ctx.guild.verification_level}**\n\n"
        f":slight_smile: Людей на сервере: **{ctx.guild.member_count}\n\n"
    )
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {ctx.guild.id}")
    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)

@bot.command()
async def profile(ctx):
	img = Image.new("RGBA", (400, 200), '#232529')
	url = str(ctx.author.avatar_url)[:-10]

	response = requests.get(url, stream = True)
	response = Image.open(io.BytesIO(response.content))
	response = response.convert("RGBA")
	response = response.resize((100, 100), Image.ANTIALIAS)

	img.paste(response, (15, 15, 115, 115))

	cursor.execute(f"SELECT balance FROM users WHERE id={ctx.message.author.id}")
	author_balance = cursor.fetchone()[0]
	cursor.execute(f"SELECT xp FROM users WHERE id={ctx.message.author.id}")
	author_xp = cursor.fetchone()[0]
	cursor.execute(f"SELECT lvl FROM users WHERE id={ctx.message.author.id}")
	author_lvl = cursor.fetchone()[0]
	idraw = ImageDraw.Draw(img)
	name = ctx.author.name
	tag = ctx.author.discriminator

	headline = ImageFont.truetype('arial.ttf', size = 20)
	undertext = ImageFont.truetype('arial.ttf', size = 12)
	need_xp = 100 + author_lvl * 0.25 * 100

	idraw.text((145, 15), f'{name}#{tag}', font=headline)
	idraw.text((145, 50), f'ID:{ctx.author.id}', font=undertext)
	idraw.text((145, 75), f'LVL: {author_lvl}', font=undertext)
	idraw.text((145, 100), f'XP: {author_xp}/{need_xp}', font=undertext)
	idraw.text((15, 145), f'Balance: {author_balance}GLC', font=headline)

	img.save('user_card.png')

	await ctx.send(file = discord.File(fp = 'user_card.png'))

@bot.command()
async def bet(ctx, amount : float):
	cursor.execute(f"SELECT balance FROM users WHERE id={ctx.message.author.id}")
	balance = cursor.fetchone()[0]

	if balance > amount and amount > 0:
		num = random.randint(1, 5)
		if num == 1 or num == 2 or num == 3:
			result = balance - amount
			await ctx.send(f"Вы проиграли {amount}GLC")
			cursor.execute(f"UPDATE users SET balance={result} WHERE id={ctx.message.author.id}")
		elif num == 4 or num == 5:
			a = amount * 2
			result = balance + a
			await ctx.send(f"Вы выиграли {a}GLC")
			cursor.execute(f"UPDATE users SET balance={result} WHERE id={ctx.message.author.id}")
	else:
		embed = discord.Embed(title = ':x: На вашем счете недостаточно средств!', color=0xeb4132)
		await ctx.send(embed=embed)

	conn.commit()

@bot.command()
@commands.has_permissions(administrator = True)
async def give(ctx, amount : int, member : discord.Member):
	cursor.execute(f"SELECT balance FROM users WHERE id={member.id}")
	balance = cursor.fetchone()[0]
	a = balance + amount
	cursor.execute(f"UPDATE users SET balance={a} WHERE id={member.id}")
	conn.commit()

@bet.error
async def bet_error(ctx, error):
    embed_error_bet = discord.Embed(title = 'Вы не указали сумму!', color=0xeb4132)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=embed_error_bet)

@bot.command()
async def buy(ctx, what=None):
	cursor.execute(f"SELECT lvl FROM users WHERE id={ctx.message.author.id}")
	lvl = cursor.fetchone()[0]
	lvl_price = 300 + lvl * 0.35 * 300

	cursor.execute(f"SELECT balance from users WHERE id={ctx.message.author.id}")
	balance = cursor.fetchone()[0]

	guild = ctx.guild
	member = ctx.message.author
	member_name = ctx.message.author.name
	category = discord.utils.get(guild.categories, name="Private")

	if what == None:
		emb = discord.Embed(title="Магазин:")
		emb.description=(
		f"1) Собственный текстовый канал: 500GLC\n\n"
		f"2) Собственный войс канал: 500GLC\n\n"
		f"3) +1 лвл(у каждого своя цена, зависящая от уровня): {int(lvl_price)}GLC\n\n"
		f'*Чтобы купить, что-то пропишите - "!buy (номер товара)"*\n\n'
		)
		await ctx.send(embed=emb)
	elif int(what) == 1:
		if balance > 500:
			channel = discord.utils.get(guild.text_channels, name=member_name.lower())
			if channel == None:
				overwrites = {
   					guild.default_role : discord.PermissionOverwrite(read_messages=False),
    				member : discord.PermissionOverwrite(read_messages=True)
    			}
				channel = await guild.create_text_channel(f"{member_name}", category=category, overwrites=overwrites)
				await ctx.send(embed = discord.Embed(title = "Ваш канал создан!", color=0x2ecc71))
				balance = balance - 500
				cursor.execute(f"UPDATE users SET balance={balance} WHERE id={ctx.message.author.id}")
			else:
   				await ctx.send(embed = discord.Embed(title = 'У вас уже есть канал!', color=0xeb4132))
		else:
   			await ctx.send(embed = discord.Embed(title = "На вашем счету недостаточно средств!", color=0xeb4132))
	elif int(what) == 2:
   		if balance > 500:
   			channel = discord.utils.get(guild.voice_channels, name=member_name)
   			if channel == None:
   				overwrites = {
   					guild.default_role : discord.PermissionOverwrite(view_channel=False),
   					member : discord.PermissionOverwrite(view_channel=True)
   				}
   				channel = await guild.create_voice_channel(f"{member_name}", category=category, overwrites=overwrites)
   				await ctx.send(embed = discord.Embed(title = "Ваш канал создан!", color=0x2ecc71))
   				balance = balance - 500
   				cursor.execute(f"UPDATE users SET balance={balance} WHERE id={ctx.message.author.id}")
   			else:
   				await ctx.send(embed = discord.Embed(title = 'У вас уже есть канал!', color=0xeb4132))
   		else:
   			await ctx.send(embed = discord.Embed(title = "На вашем счету недостаточно средств!", color=0xeb4132))
	elif int(what) == 3:
   		if balance > int(lvl_price):
   			balance = balance - lvl_price
   			lvl = lvl + 1
   			cursor.execute(f"UPDATE users SET balance={balance} WHERE id={ctx.message.author.id}")
   			cursor.execute(f"UPDATE users SET lvl={lvl} WHERE id={ctx.message.author.id}")
   			await ctx.send(embed = discord.Embed(title = f"Ваш уровень был повышен до {lvl}!", color=0x2ecc71))
   		else:
   			await ctx.send(embed = discord.Embed(title = "На вашем счету недостаточно средств!", color=0xeb4132))
   			
	conn.commit()

bot.run(config.TOKEN)