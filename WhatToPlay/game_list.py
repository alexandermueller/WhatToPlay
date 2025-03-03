#!/usr/bin/env python3

from typing import Optional

class GameList:
	def __init__(self, gameList: Optional[str] = None):
		self.gameList = [game.strip() for game in gameList.split('\n')] if gameList else []

	def description(self) -> str:
		return '\n'.join(self.gameList)
