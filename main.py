import os
import crypto

import discord 
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '$', intents = discord.Intents.all(), help_command = None)

@client.event 
async def on_ready():
  print('Logged in as {0.user}'.format(client))

crypto.setup(client)
my_secret = os.getenv('token')
client.run(my_secret)