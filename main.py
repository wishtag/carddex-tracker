import discord
from discord.ui import Select, View, Button
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import json

load_dotenv()

intents = discord.Intents().default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = ["#",":","?", ">"], intents=intents)

# ---v

default_settings = {
    "idk": 0
}
default_settings = json.dumps(default_settings, indent = 4)

def create_json(file):
    try:
        data = os.listdir("data").index(f'{file}')
    except:     
        with open(f"data/{file}", "w") as outfile:
            outfile.write(default_settings)

def read_json(file):
    try:
        f = open (f"data/{file}", "r")
        data = json.loads(f.read())
        f.close()
        return data
    except:
        create_json(file)
        f = open (f"data/{file}", "r")
        data = json.loads(f.read())
        f.close()
        return data

def write_json(file, object):
    f = open (f"data/{file}", "w")
    json.dump(object, f)
    f.close()

def value_is_none(file, value):
    data = read_json(file)
    if data[value] == None:
        return True
    else:
        return False

# ---^

@bot.command()
async def add(ctx, name, num):
    data = read_json("pokemon.json")
    if name in data:
        await ctx.send("Already in index, nothing has been added")
    else:
        temp = {name:{"name":name,"dex":num}}
        data.update(temp)
        write_json("pokemon.json", data)
        #for i in data:
        #    print(data[i]["dex"])
        await ctx.send("Entry has been added to index")

@bot.command()
async def dex(ctx, num):
    data = read_json("pokemon.json")
    notFound = True
    for i in data:
        if data[i]["dex"] == num:
            temp = i
            notFound = False
            await ctx.send("Entry found, do you want to mark this card as owned?")
            type_view = View(timeout=30)
            no_button_option = Button(label="No", style=discord.ButtonStyle.red)
            yes_button_option = Button(label="Yes", style=discord.ButtonStyle.green)
            type_view.add_item(no_button_option)
            type_view.add_item(yes_button_option)

            dis_type_view = View()
            dis_no_button_option = Button(label="No", style=discord.ButtonStyle.gray, disabled=True)
            dis_yes_button_option = Button(label="Yes", style=discord.ButtonStyle.gray, disabled=True)
            dis_type_view.add_item(dis_no_button_option)
            dis_type_view.add_item(dis_yes_button_option)

            the_buttons = await ctx.send(view=type_view)
            async def no_callback(interaction):
                await the_buttons.edit(view=dis_type_view)
                await interaction.response.defer()
            no_button_option.callback = no_callback

            async def yes_callback(interaction):
                await the_buttons.edit(view=dis_type_view)
                await interaction.response.defer()
                del data[temp]
                write_json("pokemon.json", data)
            yes_button_option.callback = yes_callback
    if notFound:
        await ctx.send("Entry not found in index, meaning you probably already own this card")

@bot.command()
async def name(ctx, difname):
    data = read_json("pokemon.json")
    notFound = True
    for name in data:
        if name == difname:
            temp = difname
            notFound = False
            await ctx.send("Entry found, do you want to mark this card as owned?")
            type_view = View(timeout=30)
            no_button_option = Button(label="No", style=discord.ButtonStyle.red)
            yes_button_option = Button(label="Yes", style=discord.ButtonStyle.green)
            type_view.add_item(no_button_option)
            type_view.add_item(yes_button_option)

            dis_type_view = View()
            dis_no_button_option = Button(label="No", style=discord.ButtonStyle.gray, disabled=True)
            dis_yes_button_option = Button(label="Yes", style=discord.ButtonStyle.gray, disabled=True)
            dis_type_view.add_item(dis_no_button_option)
            dis_type_view.add_item(dis_yes_button_option)

            the_buttons = await ctx.send(view=type_view)
            async def no_callback(interaction):
                await the_buttons.edit(view=dis_type_view)
                await interaction.response.defer()
            no_button_option.callback = no_callback

            async def yes_callback(interaction):
                await the_buttons.edit(view=dis_type_view)
                await interaction.response.defer()
                del data[temp]
                write_json("pokemon.json", data)
            yes_button_option.callback = yes_callback
    if notFound:
        await ctx.send("Entry not found in index, meaning you probably already own this card")

token = os.environ['bot_token']
bot.run(token)