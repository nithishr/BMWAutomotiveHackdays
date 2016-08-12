__author__ = 'nithishr'

import requestsDAO

class DeliveryDAO:
    def __init__(self,database):
        self.db = database
        self.deliveries = database.deliverers

    def createDelivery(self,requestId):
        res = self.deliveries.insertOne(requestId)
        return res.inserted_id


