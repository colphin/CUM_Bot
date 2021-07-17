import discord
from discord.ext import commands
import os
import RedditRelay
from decouple import config
import datetime
import atexit
import time

# Create client object
client = discord.Client()

# Get Token from enviroment
token = config('DISCORD_TOKEN')
admin = config('DISCORD_ADMIN_ID')

# Create reddit relay
redditRelay = RedditRelay.RedditRelay()
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Create Cooldown dictionary to prevent spamming
coolDownDictionary = {}

def isUserOnCoolDown(user):
    coolDownPeriod = datetime.timedelta(minutes=3)

    if coolDownDictionary[user] == None or str(user.id) == str(admin):
        coolDownDictionary[user] = datetime.datetime.now()
        return 0
    delta = datetime.datetime.now() - coolDownDictionary[user]
    if delta > coolDownPeriod:
        coolDownDictionary[user] = datetime.datetime.now()
        return 0
    else:
        return int(coolDownPeriod.total_seconds()) - int(delta.total_seconds())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    guildCount = 0
    for guild in client.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guildCount += 1
        for member in guild.members:
            coolDownDictionary[member] = None
        
    print("Bot is active in " + str(guildCount) + " guild(s)")

@client.event
async def on_message(message):
    # ignore if user is bot itself
    if message.author == client.user:
        return
    
    # meme content kekw
    if message.content.startswith('$meme'):
        cooldownTimer = isUserOnCoolDown(message.author)
        if cooldownTimer > 0:
            await message.channel.send("You are on cool down dumbass: " + str(cooldownTimer) + " seconds left")
            return 

        messageArray = message.content.split(' ')
        messageCount = len(messageArray)
        topic = ''

        if (messageCount == 2):
            topic = messageArray[1]

        await message.channel.send("Fetching meme.")

        try:
            result = await redditRelay.getMeme(topic)
            if (result['code'] == 200):
                await message.channel.send(str(message.author.name) + "\n" + result['url'])
            else:
                raise Exception("Fuck if i know")
        except Exception as e:
            print(e)
            await message.channel.send('Shits broken yo.')

    # actual fucking porn
    if message.content.startswith('$porn'):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        await message.channel.send(file=discord.File('images/Chris.jpg'))

    if message.content.startswith('$tts'):
        ctx = message.member.voice.channel
        print(ctx)


print("Bot Started")
client.run(token)