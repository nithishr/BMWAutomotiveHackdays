__author__ = 'nithishr'

class UserDAO:

    def __init__(self, database):
        self.db = database
        self.users = database.users

    def getUseridFromName(self,username):
        user = self.users.find_one({'username': username})
        print user
        if user is not None:
            return user['_id']

    def addRequest(self,username,reqId):
        res = self.users.find_one_and_update({'username': username},{'$push':{'requests':reqId}})

