#!/usr/bin/env python3

from discord import Member, Interaction, TextChannel
from typing import List, Optional, Tuple, Set

from user import User, userFor


servers = {} # { Server.id : Server }


class Server:
    def __init__(self, id: int, users: Set[int] = None):
        self.id = id
        self.users = users if users else set()

    async def userFor(self, id: int) -> User:
        if not id in self.users:
            self.users.add(id)
            # TODO: Schedule An Update To The Server In The Database

        return await userFor(id)


async def serverFor(id: int) -> Server:
    global servers

    if id not in servers:
        servers[id] = Server(id)
        # await InsertServer(server = servers[id]).execute()

    return servers[id]
