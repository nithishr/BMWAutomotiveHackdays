__author__ = 'nithishr'
import pymongo

class requestsDAO():
    def __init__(self,database):
        self.db = database
        self.req = database.requests

    def createRequest(self,userid,delId,location,time,date,duration):
        res = self.req.insert_one({'status':False, 'uid':userid, 'delId':delId,'location':location,
                              'time':time, 'date':date,'duration':duration})
        self.req.find_one_and_update({'_id':res.inserted_id},{'$push':{'id':str(res.inserted_id)}})
        return res.inserted_id

    def deleteRequest(self, reqId):
        res = self.req.delete_one({'_id':reqId})
        return res.count

    def filterRequests(self,fltr):
        res = self.req.find(fltr)
        return res

    def updateRequest(self, reqId, status=True):
        res = self.req.find_one_and_update({'id':reqId},{'$set':{'status':status}})
        print res

    def requestById(self,reqId):
        pass
