import discord
import os
import logging

from discord.ext import commands, tasks
from discord.ext.commands import Greedy, Context
from typing import Literal, Optional, List
from config import *

# Create a subclass of commands.Bot
class WhitelistBot(commands.Bot):
    def __init__(self):
       super().__init__(command_prefix=prefix,
                        intents=discord.Intents.all(),
                        activity=discord.CustomActivity(status))
       
       self.logger = logging.getLogger('discord')
       self.logger.setLevel(logging.INFO)
       handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
       handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
       self.logger.addHandler(handler)

    async def setup_hook(self):
       self.logger.info('——————————————————————')
       self.logger.info(f'Initializing {self.user}...')
       self.logger.info(f'Owner ID: {self.owner_id}')
       self.logger.info(f"Coded by: PixonGamer \n Github repo: PLACEHOLDER")
       cog_directory = 'Cogs'
       cogs_loaded = 0

       for entry in os.scandir(cog_directory):
           if entry.name.endswith('.py') and entry.is_file():
               try:
                  cog = f'{cog_directory}.{entry.name[:-3]}'
                  await self.load_extension(cog)
                  self.logger.info(f'{cog} was successfully loaded!')
                  cogs_loaded += 1
               except discord.ClientException as e:
                  self.logger.error(f'There was a problem with {cog}!, exception: {e} / {e.__traceback__}')
       self.logger.info(f'Loaded {cogs_loaded} cogs.')
       self.logger.info('Started successfully!')
       self.logger.info('——————————————————————')

    async def on_command_error(self, ctx: Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('The command you tried to use cannot be used in private messages. Please try again in a server.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. The command you tried to use is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                self.logger.exception('In %s:', ctx.command.qualified_name, exc_info=original)
            await ctx.send('An error occurred while trying to execute that command.')
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(str(error))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'You are missing a required argument (`{error.param.name}`).')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'One of the arguments (`{error.param.name}`) you provided is invalid.')
        else:
            self.logger.exception('Unhandled command error:', exc_info=error)
  

bot = WhitelistBot()

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
   """
   Thanks to Umbra for the sync command, 
   you can see what it does here: 
   https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html
   """
   if not guilds:
       synced = await sync_guild(ctx, spec)
       await ctx.send(
           f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
       )
       return

   ret = 0
   for guild in guilds:
       try:
           await ctx.bot.tree.sync(guild=guild)
       except discord.HTTPException as e:
           logging.error(f"Failed to sync commands to guild {guild.id}: {e}")
       else:
           ret += 1

   await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

async def sync_guild(ctx: commands.Context, spec: Optional[Literal["~", "*", "^"]] = None) -> List[str]:
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
   return synced


bot.run(token)
