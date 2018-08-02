import discord
import datetime
import threading
import asyncio
import queue
from qqbot import QQBotSlot as qqbotslot, RunBot


def now():
    return datetime.datetime.now().strftime('%H:%M:%S')


qqbot = None
qqgroup = None
fuduChannel = None
client = None
qqMsg = queue.Queue(0)

# ====================================================== load config

f = open('bot.cfg', 'r', encoding='utf-8')
config = f.read().replace('\n','').split('#')
f.close()

configBotToken = config[0]
configDiscordListen = config[1].split(',')
configDiscordForward = config[2].split(',')
configQQListen = config[3].split(',')
configQQForward = config[4].split(',')

print(configBotToken)
print(configDiscordListen)
print(configDiscordForward)
print(configQQListen)
print(configQQForward)

# ====================================================== qq

@qqbotslot
def onQQMessage(bot, contact, member, content):
    if bot.isMe(contact, member):
        return
    
    global configQQListen
    if contact.nick not in configQQListen:
        return

    if content == '帮助':
        bot.SendTo(contact, '我是机器人。 我负责在Discord和QQ之间架起沟通的桥梁。请勿私聊或加好友。')
        return

    qqMsg.put('[Q-' + contact.nick + '-' + member.name + '-' + now() + '] ' + content)
    # if content[0:5] == '机器人转发':
    # global fuduChannel
    # global client
    # if fuduChannel != None and client != None:
    #     await client.send_message(fuduChannel, '[QQ-' + member.name + '-' + now() + '] ' + content)
    # return


@qqbotslot
def onStartupComplete(bot):
    global qqbot
    global qqgroup
    qqbot = bot
    qqgroup = []
    for qqForwardItem in configQQForward:
        qqgroup.append(bot.List('group', qqForwardItem)[0])

    print('QQ is ready!')


# =================================================================== discord
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    global configDiscordListen
    if message.channel.id not in configDiscordListen:
        return

    if message.content.startswith('.help'):
        await client.send_message(message.channel, 'I am a bot. I am a bridge between QQ and Discord. DO NOT DM me please.')
        return

    global qqbot
    global qqgroup
    if qqbot != None and qqgroup != None:
        for qqgroupItem in qqgroup:
            qqbot.SendTo(qqgroupItem, '[D-#' + message.channel.name + '-' +message.author.name + '-' + now() + '] ' + message.content)
        return


@client.event
async def on_ready():
    print('[Discord] Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    # get correct channel
    global fuduChannel
    fuduChannel = []
    for channel in client.get_all_channels():
        if channel.id in configDiscordForward:
            fuduChannel.append(channel)

    #circle
    while True:
        try:
            cache = qqMsg.get(timeout=1, block=True)
        except:
            await asyncio.sleep(1)
            continue
        else:
            pass
        
        if fuduChannel != None and client != None:
            for fuduChannelItem in fuduChannel:
                await client.send_message(fuduChannelItem, cache)

def runQQ():
    RunBot()

def runDC():
    global configBotToken
    client.run(configBotToken)


qqthread = threading.Thread(target=runQQ, daemon=True)
dcthread = threading.Thread(target=runDC, daemon=True)

qqthread.start()
dcthread.start()

nm = input('任意键退出')
exit()
