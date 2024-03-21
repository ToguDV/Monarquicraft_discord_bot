import asyncio
import time

import discord
import os
import server_info
import dates_percent
from discord import app_commands
from dotenv import load_dotenv
from discord.ext import commands
from utils.moderation import get_modlog_kick_ban_msg

import responses

intents = discord.Intents.default()
intents.message_content = True
intents.moderation = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
dates_percent.calc_percent()

#TEST

@tree.command(
    name="progreso",
    description="¿Cuánto falta para Monarqui 5?",
    guild=discord.Object(id=788191636877344768)
)
async def progress(interaction):
    project_dir = os.path.dirname(__file__)
    images_dir = os.path.join(project_dir, 'images')
    progress_dir = os.path.join(images_dir, 'progress')
    progress_image = os.path.join(progress_dir, 'progress.png')
    file = discord.File(fp=progress_image)


    data = server_info.get_data_yml(ROOT_DIR)
    progress_work = data['progress_work']
    progress_date = data['progress_date']
    result = (progress_date + progress_work) / 2
    progress_percentage_formatted = "{:.2f}".format(result)
    await interaction.response.send_message(content=f'Progreso actual: {progress_percentage_formatted}% :D', file=file)


@tree.command(
    name="set_progress",
    description="Update server progress",
    guild=discord.Object(id=788191636877344768)
)
@app_commands.describe(value="porcentaje")
@app_commands.rename(value='valor')
async def set_progress(interaction, value:float):
    is_owner = False
    for role in interaction.user.roles:
        if role.id == 797655903746523146:
            is_owner = True
            break
        else:
            is_owner = False
    if is_owner:
        server_info.set_data("progress_work", value, ROOT_DIR)
        await interaction.response.send_message(content='Progreso guardado con éxito, Togu :)')
    else:
        await interaction.response.send_message(content='Lo siento, este comando solo está disponible para Togu :qmiedo: ')

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=788191636877344768))
    print(f'{client.user} is now running!')
    print('started')
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Monarquicraft"))


def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    client.run(TOKEN)
