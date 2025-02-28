#!/usr/bin/env python3

import os
import sys
import discord

from typing import List, Optional, Union
from discord.ext import commands
from discord import app_commands
from discord.ui import *

from constants import *
from helpers import *

################################################ Bot Init ################################################

intents = discord.Intents.default()
bot = commands.Bot(command_prefix = '/', intents = intents)

################################################ Commands ################################################

@bot.event
async def on_ready():
    logEvent('-> Logged in as "%s" - %s' % (bot.user.name, bot.user.id))
    await bot.tree.sync()

################################################ Run Bot #################################################        

def main(argc, argv):
    logEvent('-> Retrieving Bot Token:')

    if token := DISCORD_TOKEN:
        logEvent('->\ttoken was found successfully.')
        bot.run(token)
        return

    tokenFile = None

    if os.path.exists('.token.txt'):
        tokenFile = open('.token.txt', 'r')

    if tokenFile == None:
        logEvent('-> Error: Token file "./.token.txt" couldn\'t be found in ".../WhatToPlay...-".')
        logEvent('->        Generate a new token on discord for your bot and place it inside')
        logEvent('->        ".../WhatToPlay...-/.token.txt"')
        exit()

    token = tokenFile.readline()

    logEvent('->\t.token.txt was found successfully.')
    bot.run(token)

if __name__ == '__main__':
   main(len(sys.argv) - 1, sys.argv[1:])

