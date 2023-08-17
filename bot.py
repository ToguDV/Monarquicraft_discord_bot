import discord
import os
import responses
from dotenv import load_dotenv


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
    intents = discord.Intents.default()
    intents.message_content = True
    intents.moderation = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
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

    @client.event
    async def on_member_ban(guild, user):
        print("Ha sido baneado:" + user.global_name)

    client.run(TOKEN)



