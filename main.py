import discord
from discord.ext import commands

import sqlite3
import json
import ast

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents) 

@bot.command()
async def command(ctx):
    embed = discord.Embed(title='Помощь в командах', description=f'/items "Название предмета" \n \n /planets "Навзание планеты"  \n \n Общии правила: пробел заменять на "_"', color=0xE9019A)
    await ctx.send(embed=embed)

@bot.command()
async def planets(ctx, message = None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if message is None:
        cursor.execute('SELECT * FROM planets')
    else:
        name = message.replace('_',' ')
        cursor.execute('SELECT * FROM planets WHERE name = "'+name+'"')
    results = cursor.fetchall()
    for item in results:
        planet = item[1]
        resource = item[2]
        embed = discord.Embed(title=planet, description=f'Ресурсы: '+resource+'', color=0xE9019A)
        await ctx.send(embed=embed)
    connection.close()

@bot.command()
async def items(ctx, message = None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if message is None:
        cursor.execute('SELECT * FROM items')
    else:
        name = message.replace('_',' ')
        cursor.execute('SELECT * FROM items WHERE name = "'+name+'"')
    results = cursor.fetchall()
    for item in results:
        planet = ''
        title = item[1]
        comment = item[2]
        cursor.execute('SELECT * FROM planets WHERE resource LIKE "%'+title+'%"')
        results = cursor.fetchall()
        for item in results:
            planet += item[1]+" "
        embed = discord.Embed(title=title, description=f'Планеты: '+planet+'\n \n Коментарий: '+comment+'', color=0xE9019A)
        await ctx.send(embed=embed)
    connection.close()
    
@bot.command()
@commands.has_permissions(administrator = True)
async def dataupdate(ctx, *, json_text):
    json_data = json.dumps(json_text)
    try:
        await save_data(ctx, json_data)
        embed = discord.Embed(title="JSON Data", description=f'```json\n{json_text}\n```', color=0x00ff00)
        await ctx.send(embed=embed)
    except json.JSONDecodeError as e:
        await ctx.send(f'Ошибка при обработке JSON: {e}')

async def save_data(ctx, json_data):
    connection = sqlite3.connect('database.db')
    json_data = json.loads(json_data)
    json_data = ast.literal_eval(json_data)
    cursor = connection.cursor()

    if json_data['data'] == 'items':
        name_data = json_data['data']
        name_items = json_data['item']
        comment_items = json_data['comment']
        cursor.execute('INSERT INTO '+name_data+' (name, comment) VALUES (?, ?)', (name_items, comment_items))
        connection.commit()
        connection.close()
        await ctx.send(name_items+" - Успешно добавлен в базу")
        
    if json_data['data'] == 'planets':
        name_data = json_data['data']
        name_planet = json_data['name']
        resource = json_data['resource']
        cursor.execute('INSERT INTO '+name_data+' (name, resource) VALUES (?, ?)', (name_planet, resource))
        connection.commit()
        connection.close()
        await ctx.send(name_planet+" - Успешно добавлен в базу")



        


bot.run('')