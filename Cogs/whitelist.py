import discord
from discord import app_commands
from discord.ext import commands
from discord import Member
from collections import defaultdict
from config import *

class WhitelistCog(commands.Cog):
	def __init__(self, client):
		self.client = client	
		self.whitelist = set()
		self.attempts = defaultdict(int)
		self.log_channel_id = LogChannelID
	 
	@commands.hybrid_group(invoke_without_command = True)
	async def whitelist(self, ctx):
		pass


	@whitelist.command(description = "Adds a member to the whitelist.")
	@app_commands.default_permissions(administrator=True)
	@commands.has_permissions(administrator=True)	
	@app_commands.describe(user_id='The ID of the user to be added to the whitelist.')
	async def add(self, ctx, user_id):
		try:
			user = await self.client.fetch_user(user_id)		
			if user.bot:
				await ctx.send(f"User with ID {user_id} is a bot. Bots cannot be whitelisted.")
				return
			if user_id in self.whitelist:
				await ctx.send(f"User with ID {user_id} is already whitelisted.")
				return
			bans = ctx.guild.bans()
			async for ban in bans:
				if ban.user.id == user_id:
					await ctx.send(f"User with ID {user_id} ({ban.user.name}) is currently banned. Please unban them first before whitelisting.")
					return
			self.whitelist.add(user_id)
			await ctx.send(f"User with ID {user_id} has been added to the whitelist.")
			await self.send_log(ctx, f"User with ID {user_id} has been added to the whitelist by {ctx.author}.")
		except discord.NotFound:
			await ctx.send("Invalid user ID.")	


	@whitelist.command(description = "Removes a member from the whitelist.")
	@app_commands.default_permissions(administrator=True)
	@commands.has_permissions(administrator=True)	
	@app_commands.describe(user_id='The ID of the user to be removed from the whitelist.')
	async def remove(self, ctx, user_id):
		try:
			self.whitelist.remove(user_id)
			await ctx.send(f"User with ID {user_id} has been removed from the whitelist.")
			await self.send_log(ctx, f"User with ID {user_id} has been removed from the whitelist by {ctx.author}.")
		except KeyError:
			await ctx.send(f"User with ID {user_id} is not in the whitelist.")

		user = ctx.guild.get_member(user_id)
		if user:
			try:
				await user.kick(reason=f"Removed from whitelist by {ctx.author}")
			except discord.Forbidden:
				await ctx.send(f"Bot does not have permission to kick user with ID {user_id}.")



	@commands.Cog.listener()
	async def on_member_join(self, ctx, member):
		if member.bot:
			return

		if member.id not in self.whitelist:
			self.attempts[member.id] += 1

			if self.attempts[member.id] > 3:
				await member.ban(reason="Exceeded join attempts.")
				del self.attempts[member.id]
				await self.send_log(ctx, f"{member.name} has been banned for exceeding join attempts.")
			else:
				await member.kick(reason="Not on whitelist.")
				await self.send_log(ctx,f"{member.name} has been kicked for not being on the whitelist.")

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member.id in self.attempts:
			del self.attempts[member.id]

	async def send_log(self, ctx, message):
		log_channel = await ctx.guild.fetch_channel(self.log_channel_id)
		await log_channel.send(message)

async def setup(client):
	await client.add_cog(WhitelistCog(client=client))	

