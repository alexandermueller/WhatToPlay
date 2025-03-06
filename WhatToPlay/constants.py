#!/usr/bin/env python3

import os
import sys

######################################### Constants #########################################

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN', None)

PLAYER_TWO_DESCRIPTION = 'Compare your ranked list against this person\'s ranked list.'
PLAYER_THREE_DESCRIPTION = 'Also compare your ranked list against this person\'s ranked list.'
PLAYER_FOUR_DESCRIPTION = 'Also compare your ranked list against this person\'s ranked list.'
SHOW_DISCOVERY_LIST = 'Show the top 4 games from other players\' lists that didn\'t appear in yours.'

DATABASE_NAME = 'what_to_play.db'
