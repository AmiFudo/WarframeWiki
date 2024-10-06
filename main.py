import discord
from discord.ext import commands

from func_data import *
from func_check import *

import time
import sqlite3
import json
import ast

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents) 

text_command = {
    0:'/items "Название предмета" - Узнать где фармить предмет \n \n ',
    1:'/planets "Навзание планеты" - Узнать что находится на планете \n \n',
    2:'/credits - Узнать где фармить кредиты \n \n',
    3:'/mods "Название мода" - Узнать данные о моде \n \n',
    4:'/warframe "Название варфрейма" - Узнать все о варфрейме \n \n',
    5:'/companion "Название компаньёна" - Узнать все о компаньёне \n \n',
    6:'/builds "На кого хотите билд" - Узнать билд \n \n',
    7:'Общие правила: пробел заменять на "_"'
}

@bot.command()
@commands.has_any_role('Пользователь бота')
async def command(ctx):
    if not await check_chanel_id(ctx):
        return
    text_send = ''
    for i in range(8):
        text_send += text_command[i]
    embed = discord.Embed(title='Помощь в командах', description=f''+text_send+'', color=0xE9019A)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role('Пользователь бота')
async def planets(ctx, message = None):
    if not await check_chanel_id(ctx):
        return
    if message is None:
        embed = discord.Embed(title="Укажите название планеты", description=f'В этой команде нужно указывать название планеты', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    else:
        name = message.replace('_',' ')
        await get_planets(ctx, name)

@bot.command()
@commands.has_any_role('Пользователь бота')
async def items(ctx, message = None):
    if not await check_chanel_id(ctx):
        return
    if message is None:
        embed = discord.Embed(title="Укажите название предмета", description=f'В этой команде нужно указывать название предмета', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    else:
        name = message.replace('_',' ')
        await get_items(ctx, name)

@bot.command()
@commands.has_any_role('Пользователь бота')
async def warframe(ctx, message = None):
    if not await check_chanel_id(ctx):
        return
    if message is None:
        embed = discord.Embed(title="Укажите название варфрейма", description=f'В этой команде нужно указывать название варфрейма', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    else:
        name = message.replace('_',' ')
        await get_warframe(ctx, name)

@bot.command()
@commands.has_any_role('Пользователь бота')
async def mods(ctx, message = None):
    if not await check_chanel_id(ctx):
        return
    if message is None:
        embed = discord.Embed(title="Укажите название мода", description=f'В этой команде нужно указывать название мода', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    else:
        name = message.replace('_',' ')
        await get_mods(ctx, name)

@bot.command()
@commands.has_any_role('Пользователь бота')
async def companion(ctx, message = None):
    if not await check_chanel_id(ctx):
        return
    if message is None:
        embed = discord.Embed(title="Укажите название компаньёна", description=f'В этой команде нужно указывать название компаньёна', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    else:
        name = message.replace('_',' ')
        await get_companion(ctx, name)

@bot.command()
@commands.has_any_role('Пользователь бота')
async def builds(ctx, message = None):
    if not await check_chanel_id(ctx):
        return
    if message is None:
        embed = discord.Embed(title="Укажите название компаньёна", description=f'В этой команде нужно указывать название компаньёна', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    else:
        name = message.replace('_',' ')
        await get_builds(ctx, name)

@bot.command()
@commands.has_any_role('Пользователь бота')
async def credits(ctx):
    if not await check_chanel_id(ctx):
        return
    embed = discord.Embed(title="Кредиты", description=f'Фармятся везде, но в основном лучше их фармить на индексе (Нептун) и на сфере прибыли(Венера Фортуна)', color=0x445bf2)
    await ctx.send(embed=embed)
    
@bot.command()
@commands.has_permissions(administrator = True)
async def datacreate(ctx, *, json_text):
    if not await check_chanel_id(ctx):
        return
    json_data = json.dumps(json_text)
    try:
        await save_data(ctx, json_data)
        embed = discord.Embed(title="JSON Data", description=f'```json\n{json_text}\n```', color=0x00ff00)
        await ctx.send(embed=embed)
    except json.JSONDecodeError as e:
        await ctx.send(f'Ошибка при обработке JSON: {e}')

@bot.command()
@commands.has_permissions(administrator = True)
async def dataupdate(ctx, *, json_text):
    if not await check_chanel_id(ctx):
        return
    json_data = json.dumps(json_text)
    try:
        await update_data(ctx, json_data)
        embed = discord.Embed(title="JSON Data", description=f'```json\n{json_text}\n```', color=0x00ff00)
        await ctx.send(embed=embed)
    except json.JSONDecodeError as e:
        await ctx.send(f'Ошибка при обработке JSON: {e}')


bot.run('')
