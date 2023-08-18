import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

import responses

intents = discord.Intents.default()
intents.message_content = True
intents.moderation = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    if message.content == "":
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'{username} said: "{user_message}" ({channel})')

    await send_message(message, user_message, is_private=False)



@bot.command()
async def test(ctx):
    await ctx.send("webos!")

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        if response == 'No commands':
            return
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)












