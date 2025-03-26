#!/usr/bin/env python3

from backend_updates import SQLInstruction


### Users ###

class CreateUsersTable(SQLInstruction):
    command = '''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER not null,
            server_ids TEXT null,
            has_app_installed BOOLEAN not null,
            game_list TEXT null,
            created_at datetime not null default CURRENT_TIMESTAMP,
            modified_at datetime not null default CURRENT_TIMESTAMP,
            primary key (id)
        );
    '''

    def __init__(self, dropIfExists = False):
        super().__init__(beforehand = [DropUsersTable()] if dropIfExists else None)

class DropUsersTable(SQLInstruction):
    command = 'DROP TABLE IF EXISTS Users;'


### CreateModifiedAtTrigger ###

class CreateModifiedAtTrigger(SQLInstruction):
    command = '''
        CREATE TRIGGER IF NOT EXISTS modified_at
        AFTER UPDATE ON Users
        BEGIN
            UPDATE Users
                SET modified_at = CURRENT_TIMESTAMP
            WHERE id = old.id;
        END;
    '''

    def __init__(self, dropIfExists = False):
        super().__init__(beforehand = [DropModifiedAtTrigger()] if dropIfExists else None)

class DropModifiedAtTrigger(SQLInstruction):
    command = 'DROP TRIGGER IF EXISTS modified_at;'


### SetupDatabase ###

class SetupDatabase(SQLInstruction):
    command = None

    def __init__(self, dropIfExists = False):
        super().__init__(
            afterwards = [
                CreateUsersTable(dropIfExists = dropIfExists),
                CreateModifiedAtTrigger(dropIfExists = dropIfExists)
            ]
        )
