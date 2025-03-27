
import aiosqlite
import asyncio

from enum import Enum
from typing import List, Optional, Self, Tuple

from ..utilities.constants import DATABASE_NAME
from ..utilities.helpers import logException, retrieveNestedDictionary

from updates import SQLInstruction


class SQLGetJSONInstruction(SQLInstruction):
    def __init__(self, command: Optional[str] = None, inputs: Optional[Tuple] = None, beforehand: Optional[List[Self]] = None, afterwards: Optional[List[Self]] = None):
        super().__init__(command = command, inputs = inputs, beforehand = beforehand, afterwards = afterwards)

    async def execute(self):
        json = {}

        async with aiosqlite.connect(DATABASE_NAME) as database:
            try:
                for instruction in [i for i in super().getInstructions() if i.command]:
                    async with database.execute(instruction.command, instruction.inputs) as cursor:
                        await instruction.update(json = json, results = await cursor.fetchall())

                await database.commit()
            except:
                for instruction in super().getInstructions():
                    print(instruction.command, instruction.inputs)

                logException()

        return json

    async def update(self, json: dict, results: List[Tuple]):
        return

class GetUsersJSON(SQLGetJSONInstruction):
    command = '''
        SELECT
            id, server_ids, has_app_installed, game_list, modified_at
        FROM
            Users;
    '''

    async def update(self, json: dict, results: List[Tuple]):
        for (userID, serverIDs, hasAppInstalled, gameList, modifiedAt) in results:
            user = retrieveNestedDictionary(json, keys = ['users', userID])
            user['server_ids'] = serverIDs
            user['has_app_installed'] = hasAppInstalled
            user['game_list'] = gameList
            user['modified_at'] = modifiedAt


class GetDatabaseRestoreJSON(SQLGetJSONInstruction):
    command = None

    def __init__(self):
        super().__init__(
            afterwards = [
                GetUsersJSON()
            ]
        )

