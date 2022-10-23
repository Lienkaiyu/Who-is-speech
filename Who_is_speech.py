import os
import configparser
import json
import discord
from discord.ext import commands,tasks

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'))
bot = commands.Bot(config.get('prefix','command_prefix'))

@bot.event
async def on_voice_state_update(member, before, after):
  voice_channel = before.channel or after.channel
  channel_id = bot.get_channel(int(config.get('channel', 'channel_ID')))

  NicknameDictFile = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Nickname.json'))
  Nickname = json.load(NicknameDictFile)
  if str(member.id) in Nickname:
    member.nick = Nickname[str(member.id)]
  if str(member.nick) == "None":
      member.nick = member.name
  NicknameDictFile.close()

  if str(after.channel) != "None" and str(before.channel) != str(after.channel):
    await channel_id.send("{}在{}出現了".format(member.nick,after.channel))
    #print(key, value)
  elif str(after.channel) == "None":
    await channel_id.send("{}離開了".format(member.nick))

  if str(after.self_stream) == "True":
    await channel_id.send("{}正在直播".format(member.nick,after.channel))

  if str(after.self_stream) == "False" and str(before.self_stream) == "True":
    await channel_id.send("{}關掉了直播".format(member.nick,after.channel))
#  if str(after.self_mute) == "True":
#    await channel_id.send("{}不說話了🙊".format(member.nick,after.channel))
#  if str(before.self_mute) == "True" and str(after.self_mute) == "False":
#    await channel_id.send("{}開麥了🎤".format(member.nick,after.channel))

#  if str(after.self_deaf) == "True":
#    await channel_id.send("{}覺得吵🙉".format(member.nick,after.channel))
#  if str(before.self_deaf) == "True" and str(after.self_mute) == "False":
#    await channel_id.send("{}想聽瓜😍".format(member.nick,after.channel))

  if str(after.mute) == "True":
    await channel_id.send("{}被禁言了😷".format(member.nick,after.channel))
  if str(before.mute) == "True" and str(after.self_mute) == "False":
    await channel_id.send("{}允許你說話🉑".format(member.nick,after.channel))

  if str(after.deaf) == "True":
    await channel_id.send("{}被隔離了😱(絕對不是我們要講秘密不讓你聽😂)".format(member.nick,after.channel))
  if str(before.deaf) == "True" and str(after.self_mute) == "False":
    await channel_id.send("{}解除隔離🙆".format(member.nick,after.channel))

print("Bot ready")

bot.run(config.get('TOKEN','TOKEN'))
