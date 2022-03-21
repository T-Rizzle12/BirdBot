import discord
import os
import time
import discord.ext, asyncio
try:
  from rcon.source import Client
  #allows the bot to use RCON
except:
  os.system("pip install rcon")
  from rcon.source import Client
  #if the bot doesn't have RCON installed install it and try again
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
#^ basic imports for other features of discord.py and python ^
address = os.environ['ADDRESS']
#^ ADDRESS is the SERVER IP, DO NOT INCLUDE THE PORT
password = os.environ['PASSWORD']
#^ PASSWORD is the server RCON Password. This is VERY CASE SENSITIVE!!!
#PUT THE SERVER IP AND PASSWORD IN THE .env FILE THIS MAKES SURE THAT IF ANYONE GETS THE CODE FOR THE BOT THEY DONT HAVE YOUR RCON IP AND RCON PASSWORD
global client, response, players

client = discord.Client()

client = commands.Bot(command_prefix = '<') #put your own prefix here

@client.event
async def on_ready():
    print("bot online")
  #will print "bot online" in the console when the bot is online
    
@client.command()
async def ping(ctx):
  await ctx.send("pong!")
#simple command so that when you type "!ping" the bot will respond with "pong!" use this to test if the bot is working

@client.command()
#grabs all they players in the server and posts them in the channel that the bot is in
async def playerlist(ctx):
  await ctx.send("Let me check the server!")
  with Client(str(address), 27015, passwd=password) as client:
    response = client.run("players")
    await ctx.send(response)
#DO NOT TOUCH 27015 THIS IS THE DEFAULT RCON PORT OF ALL PROJECT ZOMBOID SERVERS, ONLY CHANGE THIS IF YOU CHANGE THE SERVER RCON PORT
    
@client.command()
#this allows you to send messages to server members just make sure there are no spaces inbetween the message, Example: bb/servermsg Hello-Everyone-How-Are-You-Today
async def servermsg(ctx, arg):
  await ctx.send("Let me connect to the server!")
  with Client(str(address), 27015, passwd=password) as client:
    client.run("servermsg " + arg)
    await ctx.send('Sent ' + arg + ' to the server')
    
try:
  client.run(os.getenv("TOKEN"))
except:
  print("This bot is either being rate limited on discord or an error has occured.")
#this is the main code that starts the bot 
