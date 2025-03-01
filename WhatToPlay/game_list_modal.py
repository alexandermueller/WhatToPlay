#!/usr/bin/env python3

import discord

from enum import Enum
from textwrap import dedent
from typing import List, Optional, Self

from game_list import GameList


class GameListModal(discord.ui.Modal):
    def __init__(self, gameList: Optional[GameList] = None):
        placeholder = dedent('''\
        Elden Ring
        Player One
        GTFO
        Dora The Explorer
        ''')

        super().__init__(title = f'Update Your Game List:')
        self.gameList = gameList

        self.gameListInput = discord.ui.TextInput(
            label = f'Game List:',
            style = discord.TextStyle.long,
            placeholder = placeholder,
            required = True,
            default = gameList.list if gameList else None
        )

        self.add_item(self.gameListInput)


    async def on_submit(self, interaction: discord.Interaction):
        self.gameList = GameList(gameList = self.gameListInput.value)
        await interaction.response.defer()

