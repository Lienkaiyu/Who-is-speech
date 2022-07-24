import configparser
import json
import discord
from discord.ext import commands,tasks

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
config = ConfigParser()
config.read('config.ini')

bot = commands.Bot(config.get('prefix','command_prefix'))

config = configparser.ConfigParser()
config.read('config.ini')

@bot.event
async def on_voice_state_update(member, before, after):
  voice_channel = before.channel or after.channel
  channel_id = bot.get_channel(int(config.get('channel', 'channel_ID')))
  
  NicknameDictFile = open('Nickname.json', 'r') 
  Nickname = json.load(NicknameDictFile)
  if str(member.id) in Nickname:
    member.nick = Nickname[str(member.id)]
  NicknameDictFile.close()
  
  if str(after.channel) != "None":
    await channel_id.send("{}在{}出現了".format(member.nick,after.channel))
    #print(key, value)
  elif str(after.channel) == "None":
    await channel_id.send("{}離開了".format(member.nick))

print("Bot ready")

bot.run(config.get('TOKEN','TOKEN'))