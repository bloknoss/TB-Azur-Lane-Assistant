from discord.ext import commands
import os
import json
import discord
import logging
import asyncio
from datetime import datetime


client = commands.Bot(command_prefix='tb!', intents=discord.Intents.all())

#discord.utils.setup_logging(level=logging.INFO, root=False)


@client.event
async def on_ready():
    await client.tree.sync()
    time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    print(f"[{time_now}] TB has connected to Discord succesfully.")


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            await client.load_extension(f'cogs.{filename[:-3]}')


async def main(token):
    async with client:
        await load()
        await client.start(token)

if __name__ == '__main__':
    config = open('config.json')
    data = json.load(config)
    config.close()
    token = data['token']
    asyncio.run(main(token=token))
