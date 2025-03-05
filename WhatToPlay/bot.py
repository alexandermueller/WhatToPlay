#!/usr/bin/env python3

import os
import sys
import discord

from typing import List, Optional, Union
from discord.ext import commands
from discord import app_commands
from discord.ui import *

# from backend_setup import SetupDatabase
from constants import *
from helpers import *
from game_list_modal import GameListModal


################################################ Bot Init ################################################


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = '/', intents = intents)
didSetup = False


################################################ Helpers #################################################


def logCommand():
    def predicate(interaction: discord.Interaction) -> bool:
        if not interaction:
            logException('interaction does not exist!')
            return False

        userMember = interaction.user
        guild = interaction.guild
        channel = interaction.channel
        command = interaction.command

        context = f'<{ guild.name }::#{ channel.name }>[@{ userMember.name }]: /{ command.name }'
        arguments = ''.join([f" { option['name'] }={ option['value'] }" for option in interaction.data['options']]) if 'options' in interaction.data else ''

        logEvent(context + arguments)
        return True

    return app_commands.check(predicate)

def hasFinishedSettingUp():
    def predicate(interaction: discord.Interaction) -> bool:
        return didSetup
    return app_commands.check(predicate)


################################################ Commands ################################################

## LIST ##

@app_commands.guild_only()
@logCommand()
@hasFinishedSettingUp()
@bot.tree.command(name = 'list', description = f'Update your ranked games list.')
@app_commands.describe()
async def _list(interaction: discord.Interaction):
    gameListModal = GameListModal()

    await interaction.response.send_modal(gameListModal)
    await gameListModal.wait()

    gameList = gameListModal.gameList

    return await interaction.followup.send(
        content = f'Your game list:\n```{ gameList.description() }```',
        ephemeral = True
    )


############################################### Error ###################################################


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if not didSetup:
        return await interaction.response.send_message(content = 'Oops, you caught me in the middle of an update! Please try again in a few seconds.', ephemeral = True)

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(content = "You are not able to use this command.", ephemeral = True)

    logException()


################################################ Events ##################################################


@bot.event
async def on_ready():
    global didSetup

    if not didSetup:
        if os.path.exists('what_to_play.db'):
            logEvent('-> Rebuilding Players from database...')
            # await restorePlayers(bot = bot)
        else:
            logEvent('-> Building Database...')
            # await SetupDatabase().execute()

        didSetup = True

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

