#!/usr/bin/env python3

from typing import Optional

from game_list import GameList


users = {} # { User.id : User }


class User:
	def __init__(self, id: int, gameList: Optional[GameList] = None, hasAppInstalled: bool = False):
		self.id = id
		self.gameList = gameList
		self.hasAppInstalled = hasAppInstalled

	async def setGameList(self, gameList: Optional[GameList]):
		self.gameList = gameList
		# TODO: Schedule Gamelist Update Into Database Here


async def userFor(id: int, hasAppInstalled: bool = False) -> User:
	global users

	if id not in users:
	    users[id] = User(id, hasAppInstalled = False)
	    # TODO: Schedule An Insert User Into Database Here

	return users[id]
