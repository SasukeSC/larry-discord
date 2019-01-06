import discord #imports discords module
from discord.ext import commands #that^ part 2
from forecastiopy import * #imports darksky api
import urllib.request, json 
import random
import sys


darkSkyAPIKey = "1b4d6c31fe4b6ee6048fb882fccfbb1c"
botColor = 0x6ee835
botToken = ""

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='py;', description=description)#makes a new instance of a bot

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='with Python'))

@bot.command()#defines new command
async def weather(location : str):
    """Adds two numbers together."""
    with urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=" + location + "&key=AIzaSyA284UZT37ThoOi4ZM8g8gGnmgv2lx0tZc") as url:
        data = json.loads(url.read().decode())
        print(data)
    locationLat = data["results"][0]["geometry"]["location"]["lat"]
    locationLong = data["results"][0]["geometry"]["location"]["lng"]

    fio = ForecastIO.ForecastIO(darkSkyAPIKey,
                            units=ForecastIO.ForecastIO.UNITS_US,
                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
                            latitude=locationLat, longitude=locationLong)

    if fio.has_currently() is True:
	    currently = FIOCurrently.FIOCurrently(fio)
	    print('Currently')
        #await bot.say("Weather: " + currently.summary + " Temperature: " + currently.temperature)
	    for item in currently.get().keys():
	    	print(item + ' : ' + str(currently.get()[item]))
	    # Or access attributes directly
	    print(currently.temperature)
	    print(currently.summary)
    else:
	    print('No Currently data')
    
    em = discord.Embed(title="My Forecast", description='Weather: ' + str(currently.summary) + ' Temperature: ' + str(currently.temperature), colour=botColor)
    em.set_author(name='Larry', icon_url=bot.user.default_avatar_url)
    await bot.say(embed=em)
    #await bot.say("Weather: " + str(currently.summary) + " Temperature: " + str(currently.temperature))

@bot.command()
async def stop():
    """Shut bot down."""
    sys.exit()

@bot.command(pass_context=True, no_pm=True)
async def debug(self, ctx):
    """dev"""
    await bot.say(ctx.message.author.name) # <- broken

bot.run(botToken)
