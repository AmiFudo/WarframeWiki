import sqlite3
import json
import ast
import discord

# Запрос данных о билде
async def get_builds(ctx, message):
    print(1)
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM builds WHERE whom = "'+message+'"')
    results = cursor.fetchall()
    if not results:
        embed = discord.Embed(title="Таких данных нет", description=f'Попробуйте другие данные', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    for item in results:
        title = item[1]
        mods = item[2]
        mods = mods.split(', ')
        whom = item[3]
        for mod in mods:
            cursor.execute('SELECT * FROM mods WHERE name = "'+mod+'"')
            results = cursor.fetchall()
            for item_mod in results:
                embed = discord.Embed(title=title, description=f''+item_mod[1]+'', color=0xE9019A)
                embed.set_image(url=''+item_mod[2]+'')
                await ctx.send(embed=embed)

    connection.close()

# Запрос данных о компаньене
async def get_companion(ctx, message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM companion WHERE name = "'+message+'"')
    results = cursor.fetchall()
    if not results:
        embed = discord.Embed(title="Таких данных нет", description=f'Попробуйте другие данные', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    for item in results:
        title = item[1]
        comment = item[2]
        img = item[3]
        embed = discord.Embed(title=title, description=f''+comment+'', color=0xE9019A)
        embed.set_image(url=''+img+'')
        await ctx.send(embed=embed)
    connection.close()

# Запрос данных о моде 
async def get_mods(ctx, message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM mods WHERE name = "'+message+'"')
    results = cursor.fetchall()
    if not results:
        embed = discord.Embed(title="Таких данных нет", description=f'Попробуйте другие данные', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    for item in results:
        title = item[1]
        img = item[2]
        embed = discord.Embed(title=title, description=f'', color=0xE9019A)
        embed.set_image(url=''+img+'')
        await ctx.send(embed=embed)
    connection.close()

# Запрос данных о варфрейме 
async def get_warframe(ctx, message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM warframe WHERE name = "'+message+'"')
    results = cursor.fetchall()
    if not results:
        embed = discord.Embed(title="Таких данных нет", description=f'Попробуйте другие данные', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    for item in results:
        title = item[1]
        prime = item[2]
        img = item[3]
        if prime == 1:
            prime = 'Прайм версия есть'
        if prime == 2:
            prime = 'Умбра версия есть'
        if prime == 0:
            prime = 'Прайм версии нет'
        embed = discord.Embed(title=title, description=f''+prime+'', color=0xE9019A)
        embed.set_image(url=''+img+'')
        await ctx.send(embed=embed)
    connection.close()

# Запрос данных о предмете 
async def get_items(ctx, message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM items WHERE name = "'+message+'"')
    results = cursor.fetchall()
    if not results:
        embed = discord.Embed(title="Таких данных нет", description=f'Попробуйте другие данные', color=0xE9019A)
        await ctx.send(embed=embed)
        return
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

# Запрос данных о планетах 
async def get_planets(ctx, message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM planets WHERE name = "'+message+'"')
    results = cursor.fetchall()
    if not results:
        embed = discord.Embed(title="Таких данных нет", description=f'Попробуйте другие данные', color=0xE9019A)
        await ctx.send(embed=embed)
        return
    for item in results:
        planet = item[1]
        resource = item[2]
        embed = discord.Embed(title=planet, description=f'Ресурсы: '+resource+'', color=0xE9019A)
        await ctx.send(embed=embed)
    connection.close()


# Обновление данных в базе
async def update_data(ctx, json_data):
    connection = sqlite3.connect('database.db')
    json_data = json.loads(json_data)
    json_data = ast.literal_eval(json_data)
    cursor = connection.cursor()

    if json_data['data'] == 'items':
        name_data = json_data['data']
        name_items = json_data['item']
        comment_items = json_data['comment']
        cursor.execute('UPDATE '+name_data+' SET comment = "'+comment_items+'" WHERE name = "'+name_items+'"')
        connection.commit()
        connection.close()
        await ctx.send(name_items+" - Успешно обновлено в базе")
    
    if json_data['data'] == 'planets':
        name_data = json_data['data']
        name_planet = json_data['name']
        resource = json_data['resource']
        cursor.execute('UPDATE '+name_data+' SET resource = "'+resource+'" WHERE name = "'+name_planet+'"')
        connection.commit()
        connection.close()
        await ctx.send(name_planet+" - Успешно обновлено в базе")

# Создание данных в базе
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
    
    if json_data['data'] == 'warframe':
        name_data = json_data['data']
        name_warframe = json_data['name']
        prime = json_data['prime']
        image = json_data['image']
        cursor.execute('INSERT INTO '+name_data+' (name, prime, image) VALUES (?, ?, ?)', (name_warframe, prime, image))
        connection.commit()
        connection.close()
        await ctx.send(name_warframe+" - Успешно добавлен в базу")

    if json_data['data'] == 'companion':
        name_data = json_data['data']
        name_companion = json_data['name']
        comment = json_data['comment']
        image = json_data['image']
        cursor.execute('INSERT INTO '+name_data+' (name, comment, image) VALUES (?, ?, ?)', (name_companion, comment, image))
        connection.commit()
        connection.close()
        await ctx.send(name_companion+" - Успешно добавлен в базу")
    
    if json_data['data'] == 'builds':
        name_data = json_data['data']
        name_build = json_data['name']
        mods = json_data['mods']
        whom = json_data['whom']
        cursor.execute('INSERT INTO '+name_data+' (name, mods, whom) VALUES (?, ?, ?)', (name_build, mods, whom))
        connection.commit()
        connection.close()
        await ctx.send(name_build+" - Успешно добавлен в базу")