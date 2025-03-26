#!/usr/bin/env python3

import discord

from backend_retrieval import GetDatabaseRestoreJSON
from backend_updates import *
from constants import *
from helpers import *
from session import currentSession

from user import userFor
from game_list import GameList


async def restoreUsers(bot: discord.ext.commands.Bot):
    class IDWrapper:
        def __init__(self, id):
            self.id = id

    guilds = { guild.id : guild for guild in bot.guilds }

    pruneUserServerIDs = []
    pruneUsers = []

    json = await GetDatabaseRestoreJSON().execute()
    # logDictionary(json)

    currentSession().isRestoringUsers = True

    for (userID, userJSON) in json.get('users', {}).items():
        serverIDs = set()
        serverIDsString = userJSON.get('server_ids')
        hasAppInstalled = userJSON.get('has_app_installed')
        updateServerIDs = False

        for serverIDString in (serverIDsString.split(',') if serverIDsString else []):
            try:
                serverID = int(serverIDString)

                if not guilds.get(serverID):
                    updateServerIDs = True
                    continue

                serverIDs.add(serverID)
            except:
                logException()
                updateServerIDs = True

        if not serverIDs:
            if not hasAppInstalled or yearsSinceDatetime(dateFromString(userJSON.get('modified_at').split(' ')[0])) > PRUNE_USER_THRESHOLD_YEARS:
                pruneUsers.append(IDWrapper(userID))
                continue

        user = await userFor(
            id = userID,
            serverIDs = serverIDs,
            hasAppInstalled = hasAppInstalled,
            gameList = GameList.fromFormattedList(formattedList = userJSON.get('game_list'))
        )

        if updateServerIDs:
            pruneUserServerIDs.append(user)

    for user in pruneUsers:
        logEvent(f'-> Deleting User: { user.id }')
        DeleteUser(user = user).schedule(force = True)

    for user in pruneUserServerIDs:
        logEvent(f'-> Updating User: { user.id }')
        UpdateUserDetails(user = user).schedule(force = True)

    currentSession().isRestoringUsers = False
