
from typing import List, Optional, Set, Tuple, Union

from ..backend.updates import InsertUser, UpdateUserDetails

from game_list import GameList


users = {} # { User.id : User }


ServerIDs = Union[Set[int], List[int]]

class User:
	def __init__(self, id: int, serverIDs: Optional[ServerIDs] = None, hasAppInstalled: bool = False, gameList: Optional[GameList] = None):
		self.id = id
		self.serverIDs = set(serverIDs) if serverIDs else set()
		self.hasAppInstalled = hasAppInstalled
		self.gameList = gameList

	async def addServerID(self, serverID: int):
		if serverID not in self.serverIDs:
			self.serverIDs.add(serverID)
			await UpdateUserDetails(user = self).execute()

	async def removeServerID(self, serverID: int):
		if serverID in self.serverIDs:
			self.serverIDs.remove(serverID)
			await UpdateUserDetails(user = self).execute()

	def formattedServerIDList(self) -> Optional[str]:
		return ','.join([str(id) for id in sorted(self.serverIDs)]) if self.serverIDs else None

	async def setHasAppInstalled(self, hasAppInstalled: bool):
		if self.hasAppInstalled != hasAppInstalled:
			self.hasAppInstalled = hasAppInstalled
			await UpdateUserDetails(user = self).execute()

	def hasGameList(self) -> bool:
		return self.gameList and self.gameList.list

	async def setGameList(self, gameList: Optional[GameList]):
		self.gameList = gameList
		await UpdateUserDetails(user = self).execute()

	def formattedGameList(self) -> Optional[str]:
		return self.gameList.formattedList() if self.gameList else None

	def formattedData(self) -> Tuple[int, Optional[str], bool, Optional[str]]:
		return (
			self.id,
			self.formattedServerIDList(),
			self.hasAppInstalled,
			self.formattedGameList()
		)

async def fetchUser(id: int) -> Optional[User]:
	return users.get(id)

async def userFor(id: int, serverIDs: Optional[ServerIDs] = None, hasAppInstalled: bool = False, gameList: Optional[GameList] = None) -> User:
	global users

	if id not in users:
	    users[id] = User(id = id, serverIDs = serverIDs, hasAppInstalled = hasAppInstalled, gameList = gameList)
	    await InsertUser(user = users[id]).execute()

	return users[id]
