# Imports
import discord
import asyncio
import os
from typing import Literal, Optional
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from dotenv import load_dotenv

intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", intents=intents)

client.remove_command('help')

member = discord.Member
getcurrentwd = os.getcwd()

@client.event
async def on_ready():
  await client.change_presence(
    activity=discord.Activity(
    type=discord.ActivityType.watching, name="history unfold | .help"
    )
  )
  print('Bot is online')
  for f in os.listdir(".\cogs"):
    if f.endswith(".py"):
      await client.load_extension("cogs." + f[:-3])


@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
  if not guilds:
    if spec == "~":
      synced = await ctx.bot.tree.sync(guild=ctx.guild)
    elif spec == "*":
      ctx.bot.tree.copy_global_to(guild=ctx.guild)
      synced = await ctx.bot.tree.sync(guild=ctx.guild)
    elif spec == "^":
      ctx.bot.tree.clear_commands(guild=ctx.guild)
      await ctx.bot.tree.sync(guild=ctx.guild)
      synced = []
    else:
      synced = await ctx.bot.tree.sync()

    await ctx.send(
        f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
    )
    return

  ret = 0
  for guild in guilds:
    try:
      await ctx.bot.tree.sync(guild=guild)
    except discord.HTTPException:
      pass
    else:
      ret += 1

  await ctx.send(f"Commands Synced.")

# load_dotenv()
# key = os.getenv("TOKEN")
# client.run(str(key))