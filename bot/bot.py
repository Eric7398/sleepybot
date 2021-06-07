import os
import discord
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents(
    messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=['e ', 'E '], intents=intents)

stat = cycle([
    "____________➖⚫➖_",
    "___________➖⚫➖__",
    "__________➖⚫➖___",
    "_________➖⚫➖____",
    "________➖⚫➖_____",
    "_______➖⚫➖______",
    "______➖⚫➖_______",
    "_____➖⚫➖________",
    "____➖⚫➖_________",
    "___➖⚫➖__________",
    "__➖⚫➖___________",
    "_➖⚫➖____________",
    "__➖⚫➖___________",
    "___➖⚫➖__________",
    "____➖⚫➖_________",
    "_____➖⚫➖________",
    "______➖⚫➖_______",
    "_______➖⚫➖______",
    "________➖⚫➖_____",
    "_________➖⚫➖____",
    "__________➖⚫➖___",
    "___________➖⚫➖__",
])


@client.event
async def on_ready():
    change_status.start()
    print(f"{client.user} is online!")


@tasks.loop(seconds=3.5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(stat)))


@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.channel.purge(limit=1)
    print(f'"{extension}" Loaded')


@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.channel.purge(limit=1)
    print(f'"{extension}" Unloaded')


@client.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.channel.purge(limit=1)
    print(f'"{extension}" Reloaded')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(TOKEN)
