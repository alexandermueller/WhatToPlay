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
from server import *
from user import User, fetchUser, userFor

from game_list_modal import GameListModal
from ranked_games import rankedGames


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

        context = f'{ f"<{ guild.name }::#{ channel.name }>" if interaction.is_guild_integration() else "" }[@{ userMember.name }]: /{ command.name }'
        arguments = ''.join([f" { option['name'] }={ option['value'] }" for option in interaction.data['options']]) if 'options' in interaction.data else ''

        logEvent(context + arguments)
        return True

    return app_commands.check(predicate)

def hasFinishedSettingUp():
    def predicate(interaction: discord.Interaction) -> bool:
        return didSetup
    return app_commands.check(predicate)

async def fetchUserFor(interaction: discord.Interaction) -> User:
    if interaction.is_guild_integration() and (server := await serverFor(interaction.guild.id)):
        return await server.userFor(interaction.user.id)
    else:
        return await userFor(interaction.user.id, hasAppInstalled = True)


################################################ Commands ################################################


## LIST ##

@logCommand()
@hasFinishedSettingUp()
@bot.tree.command(name = 'list', description = f'Update your ranked multiplayer games list.')
async def _list(interaction: discord.Interaction):
    user = await fetchUserFor(interaction = interaction)
    gameListModal = GameListModal(gameList = user.gameList)

    await interaction.response.send_modal(gameListModal)
    await gameListModal.wait()

    gameList = gameListModal.gameList
    await user.setGameList(gameList = gameList)

    return await interaction.followup.send(
        content = f'Your ranked multiplayer games list was updated successfully:\n```{ gameList.description(showRanks = True) }```',
        ephemeral = True
    )


## WITH ##

@logCommand()
@hasFinishedSettingUp()
@bot.tree.command(name = 'with', description = f'Generate a new mutually-ranked multiplayer games list.')
@app_commands.describe(
    player_two = PLAYER_TWO_DESCRIPTION,
    player_three = PLAYER_THREE_DESCRIPTION,
    player_four = PLAYER_FOUR_DESCRIPTION,
    show_discovery_list = SHOW_DISCOVERY_LIST
)
async def _with(
    interaction: discord.Interaction,
    player_two: discord.Member,
    player_three: Optional[discord.Member],
    player_four: Optional[discord.Member],
    show_discovery_list: Optional[bool] = False
):
    gameLists = []
    players = [interaction.user, player_two, player_three, player_four]

    for player in players:
        if not player:
            continue

        if player.id == interaction.user.id and (user := await fetchUserFor(interaction = interaction)):
            if not user.hasGameList():
                return await interaction.response.send_message(
                    content = 'Your ranked multiplayer games list is empty.',
                    ephemeral = True
                )
        elif not (user := await fetchUser(id = player.id)) or not user.hasGameList():
            return await interaction.response.send_message(
                content = f'{ player.mention } does not have a ranked multiplayer games list.',
                ephemeral = True
            )

        gameLists += [user.gameList]

    await interaction.response.defer(ephemeral = True, thinking = True)

    return await interaction.followup.send(
        content = rankedGames(gameLists = gameLists, discoveryTopN = 4 if show_discovery_list else 0).description(), 
        ephemeral = True
    )


############################################### Error ###################################################


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if not didSetup:
        return await interaction.response.send_message(
            content = 'Oops, you caught me in the middle of an update! Please try again in a few seconds.',
            ephemeral = True
        )

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            content = "You are not able to use this command.",
            ephemeral = True
        )

    logException()


################################################ Events ##################################################


# TODO: Add event handlers for when the bot is installed/uninstalled from guilds/users

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

