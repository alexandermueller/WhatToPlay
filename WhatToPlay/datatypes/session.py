
import threading

from ..utilities.helpers import delete, get


sessions = {} # { Thread.id : Session }


class Session:
    def __init__(self):
        self.isRestoringUsers = False

    def canSendMessages(self) -> bool:
        return not self.isRestoringUsers

    def canUpdateBackend(self) -> bool:
        return not self.isRestoringUsers


def removeCurrentSession():
    global sessions
    delete(sessions, threading.get_native_id())

def currentSession() -> Session:
    global sessions
    threadID = threading.get_native_id()

    if session := sessions.get(threadID):
        return session

    sessions[threadID] = Session()
    return sessions[threadID]
