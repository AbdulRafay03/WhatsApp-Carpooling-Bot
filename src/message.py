import Config
import requests
from datetime import datetime

class Message:
    def __init__(self , messageId, text, timestamp, sender_number ,sender_name):
        self.messageId = messageId
        self.text = text
        self.timestamp = timestamp
        self.sender_name = sender_name
        self.sender_number = sender_number


        # self.label = None
        # self.departure_time = None
        # self.locations = []
        # self.destination = None



class OfferMessage(Message):
    def __init__(self, messageId, text, timestamp, sender_number, sender_name, departure_time, locations, destination):
        super().__init__(messageId, text, timestamp, sender_number, sender_name)
        self.departure_time = departure_time
        self.locations = locations
        self.destination = destination

    def to_dict(self):
        return {
            "messageId": self.messageId,
            "text": self.text,
            "timestamp": self.timestamp,
            "sender_number": self.sender_number,
            "sender_name": self.sender_name,
            "departure_time": self.departure_time,
            "locations": self.locations,
            "destination": self.destination
        }

class RequestMessage(Message):
    def __init__(self, messageId, text, timestamp, sender_number, sender_name, departure_time, locations, destination):
        super().__init__(messageId, text, timestamp, sender_number, sender_name)
        self.departure_time = departure_time
        self.locations = locations
        self.destination = destination


    def getMatch(self , OfferArray):
        Matches = []
        
        for i in OfferArray:
            print("checking Matches")
            if self.departure_time == i.departure_time:
                print("Dep match")
                print(i.locations)

                if any(loc in i.locations for loc in self.locations):
                    print("match found")
                    Matches.append(i)

        if Matches:

            headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "authorization": f"Bearer {Config.TOKEN}"
                }

            for offer in Matches:
                payload = {        
                    "body": f"Match Found for message {self.text} \nOffer: \nSenders Number: {offer.sender_number} \nSender's Name: {offer.sender_name} \nMessage: {offer.text} ",
                    "to": self.sender_number
                }
                response = requests.post(Config.URL, json=payload, headers=headers)
                print(response.text)
                return True
        else: 
            return False
                    

    def getMatch_single(self , offer): #when only one offer to match
        
        Match = None
        print("checking Matches")
        fmt = "%H:%M"
        self_time = datetime.strptime(self.departure_time, fmt)
        offer_time = datetime.strptime(offer.departure_time, fmt)
        if abs((self_time - offer_time).total_seconds()) <= 3600:
            print("Dep match")

            print(offer.locations)
            
            if any(loc in offer.locations for loc in self.locations):
                print("match found")
                Match = offer

        if Match:
            headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "authorization": f"Bearer {Config.TOKEN}"
                }

            
            payload = {        
                "body": f"Match Found for message {self.text} \nOffer: \nSenders Number: {offer.sender_number} \nSender's Name: {offer.sender_name} \nMessage: {offer.text} ",
                "to": self.sender_number
            }
            response = requests.post(Config.URL, json=payload, headers=headers)
            print(response.text)
            return True
        else: 
            return False


    




    








    