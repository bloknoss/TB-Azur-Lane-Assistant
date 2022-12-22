from discord.ext import commands
import discord
import asyncio
import os
import json

client = commands.Bot(command_prefix='tb!',intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    print("TB has connected to Discord succesfully.")

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
