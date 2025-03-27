
import aiosqlite
import asyncio

from typing import List, Optional, Self, Tuple

from ..utilities.constants import DATABASE_NAME
from ..utilties.helpers import logException
from ..utilities.session import currentSession


class SQLInstruction:
    command: str

    def __init__(self, command: Optional[str] = None, inputs: Optional[Tuple] = None, beforehand: Optional[List[Self]] = None, afterwards: Optional[List[Self]] = None):
        self.command = command if command else self.command
        self.inputs = inputs
        self.beforehand = beforehand if beforehand else list()
        self.afterwards = afterwards if afterwards else list()

    def getInstructions(self):
        return self.beforehand + [self] + self.afterwards

    async def execute(self, force = False):
        if not (currentSession().canUpdateBackend() or force):
            return

        async with aiosqlite.connect(DATABASE_NAME) as database:
            try:
                # TODO: Uncomment when foreign keys are necessary
                # await database.execute('PRAGMA foreign_keys = 1;')

                for instruction in self.getInstructions():
                    if instruction.command:
                        await database.execute(instruction.command, instruction.inputs)

                await database.commit()
            except:
                for instruction in self.getInstructions():
                    print(instruction.command, instruction.inputs)

                logException()

    def schedule(self, force = False):
        if not (currentSession().canUpdateBackend() or force):
            return

        asyncio.create_task(self.execute(force = force))


### Users ###

class InsertUser(SQLInstruction):
    command = '''
        INSERT OR IGNORE INTO
            Users (id, server_ids, has_app_installed, game_list)
        VALUES
            (?,?,?,?);
    '''

    def __init__(self, user: 'User'):
        super().__init__(
            inputs = user.formattedData()
        )

class DeleteUser(SQLInstruction):
    command = 'DELETE FROM Users WHERE id = ?;'

    def __init__(self, user: 'User'):
        super().__init__(inputs = (user.id,))

class UpdateUserDetails(SQLInstruction):
    command = '''
        UPDATE
            Users
        SET
            server_ids = ?, has_app_installed = ?, game_list = ?
        WHERE
            id = ?;
    '''

    def __init__(self, user: 'User'):
        super().__init__(inputs = (user.formattedServerIDList(), user.hasAppInstalled, user.formattedGameList(), user.id))

