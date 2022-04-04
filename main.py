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
global client, response, players, online
online = True

client = discord.Client()

client = commands.Bot(command_prefix = '<') #put your own prefix here

@client.event
async def on_ready():
    print("bot online")
    while online == True:
      for I in range(0,33):
        try:
          with Client(str(address), 27015, passwd=password, timeout=1.5) as rcon:
            response = rcon.run("players")
            print(response)
            number = str(I)
          if number in response:
            game = discord.Activity(type=discord.ActivityType.watching, name=(number + "/32 player(s)"))
            await client.change_presence(status=discord.Status.online, activity=game)
            await asyncio.sleep(0.1)
        except:
          game = discord.Activity(type=discord.ActivityType.watching, name=("Server Offline"))
          await client.change_presence(status=discord.Status.idle, activity=game)
          await asyncio.sleep(1)
          break
    await asyncio.sleep(5)
  #will print "bot online" in the console when the bot is online this will also show how many players are in the server as its status
    
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
    
@client.command()
async def adduser(ctx, arg, arg2):
  await ctx.message.delete()
  await ctx.author.send("Ok, let me add that user to the server.")
  with Client(str(address), 27015, passwd=password) as rcon:
   try:
    response = rcon.run("adduser " + arg + " " + arg2)
    await ctx.author.send('Added user with the name ' + arg + ' to the server')
    await ctx.author.send(response)
   except:
     await ctx.author.send("An error occurred or that user already exists.")
     await ctx.author.send("bb/adduser username password")
    
try:
  client.run(os.getenv("TOKEN"))
except:
  print("This bot is either being rate limited on discord or an error has occured.")
#this is the main code that starts the bot 
