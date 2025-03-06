#!/usr/bin/env python3

from typing import Optional

from game_list import GameList


users = {} # { User.id : User }


class User:
	def __init__(self, id: int, gameList: Optional[GameList] = None, hasAppInstalled: bool = False):
		self.id = id
		self.gameList = gameList
		self.hasAppInstalled = hasAppInstalled

	def hasGameList(self) -> bool:
		return self.gameList and self.gameList.list

	async def setGameList(self, gameList: Optional[GameList]):
		self.gameList = gameList
		# TODO: Schedule Gamelist Update Into Database Here


async def fetchUser(id: int) -> Optional[User]:
	if id not in users:
		return None

	return users[id]

async def userFor(id: int, hasAppInstalled: bool = False) -> User:
	global users

	if id not in users:
	    users[id] = User(id, hasAppInstalled = False)
	    # TODO: Schedule An Insert User Into Database Here

	return users[id]
