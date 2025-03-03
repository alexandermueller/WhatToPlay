#!/usr/bin/env python3

import traceback

########################################## Helpers ##########################################

def chunks(thing, n):
    return [thing[i:i + n] for i in range(0, len(thing), n)]

def logEvent(string):
    print(string)

# TODO: this could send an error report to me via DM.
def logException(string = None):
    logEvent('-> Exception Encountered: ' + ('\n' + traceback.format_exc()) if not string else string)

def describeCollection(collection):
    count = len(collection)

    if len(collection) == 0:
        return []
    
    return (', '.join(collection[:-1]) + (', and ' if count > 2 else ' and ') + collection[-1]) if count > 1 else collection[0]

def delete(dictionary, key):
    if key and key in dictionary:
        del dictionary[key]

def get(array, index, default = None):
  if not (0 <= index < len(array)):
    return default

  try:
    return array[index]
  except IndexError:
    return default

def retrieveNestedDictionary(dictionary, keys):
    if not keys:
        return None

    value = dictionary

    for key in keys:
        if key not in value:
            value[key] = {}

        value = value[key]

    return value
