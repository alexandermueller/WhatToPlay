#!/usr/bin/env python3

from typing import List, Optional

from game_list import GameList


class RankedGames:
	def __init__(self, gameList: List[str], discoveryList: List[str]):
		self.gameList = gameList
		self.discoveryList = discoveryList

	def description(self) -> str:
		rankedGamesList = [f'{ i + 1 }. { game }' for (i, game) in enumerate(self.gameList)]

		# Weird backtick bug eats the first character
		discoveryListDescription = ('\nA few of the top games that did not appear in your list:```\n' + '\n'.join(self.discoveryList) + '```') if self.discoveryList else ''

		# Weird backtick bug eats the first character
		return 'Games you should play together (in order of mutual-preference):```\n' + '\n'.join(rankedGamesList) + '```' + discoveryListDescription


def rankedGames(gameLists: List[GameList], discoveryTopN: int, userList: GameList) -> Optional[RankedGames]:
	class Game:
		def __init__(self, rank: float, name: str):
			self.rank = rank
			self.name = name

	lists = [gameList.list for gameList in gameLists]
	shared = set(lists[0])
	ranked = {}

	for l in lists[1:]:
		shared = shared.intersection(set(l))

	if not shared:
		return None

	discovery = set()

	for l in lists:
		j = 0
		count = len(l)

		for (i, name) in enumerate(l):
			if not name in shared:
				if j < discoveryTopN:
					discovery.add(name)
					j += 1

				continue

			if not name in ranked:
				ranked[name] = Game(
					rank = (i + 1) / count,
					name = name
				)
			else:
				ranked[name].rank += (i + 1) / count

	games = {}

	for game in ranked.values():
		if game.rank not in games:
			games[game.rank] = [game.name]
			continue

		games[game.rank] += [game.name]

	return RankedGames(
		gameList = [', '.join(sorted(games[rank])) for rank in sorted(games.keys())],
		discoveryList = sorted(discovery - set(userList.list))
	)
