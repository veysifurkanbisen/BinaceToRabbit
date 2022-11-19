import datetime

class UserQueue():
    eixsting_users = []
    
    def __init__(self, user_name, symbol):
        self.user_name = user_name
        self.symbol = symbol

    def start_feeding(self, queue):
        self.eixsting_users.append(queue)
        
        now = datetime.datetime.utcnow()
        response = "Started feeding the queues for the user {} at time {} !".format(queue.user_name, now)
        return response

    def stop_feeding(self, user):
        
        now = datetime.datetime.utcnow()
        response = "Stoped feeding the queues for the user {} at time {} !".format(user.user_name, now)
        return response