#!/usr/bin/env python3

import discord

########################################## Helpers ##########################################

def chunks(thing, n):
    return [thing[i:i + n] for i in range(0, len(thing), n)]

def logEvent(string):
    print(string)

def describeCollection(collection):
    count = len(collection)

    if len(collection) == 0:
        return []
    
    return (', '.join(collection[:-1]) + (', and ' if count > 2 else ' and ') + collection[-1]) if count > 1 else collection[0]

async def getDMChannelFor(user):
    if not user:
        return None
        
    return await user.create_dm() if not user.dm_channel else user.dm_channel

def getMentionableNameStringFrom(member):
    return '@%s#%s' % (member.name, member.discriminator)
