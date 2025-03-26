#!/usr/bin/env python3

from typing import Optional, Self


class GameList:
	def __init__(self, gameList: Optional[str] = None):
		self.list = []

		if not gameList:
			return

		seen = set()

		for game in [game.strip() for game in gameList.split('\n') if game]:
			if game in seen:
				continue

			seen.add(game)
			self.list += [game]

	def description(self, showRanks = False) -> str:
		return '\n'.join([f'{ i + 1 }. { game }' for (i, game) in enumerate(self.list)] if showRanks else self.list) if self.list else ''

	def formattedList(self) -> Optional[str]:
		return '\n'.join(self.list) if self.list else None

	@staticmethod
	def fromFormattedList(formattedList: Optional[str]) -> Optional[Self]:
		return GameList(gameList = formattedList) if formattedList else None
