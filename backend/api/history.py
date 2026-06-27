from datetime import datetime

class HistoryManager:

    def __init__(self):
        self.logs = []

    def add_entry(self, user, action, data):
        entry = {
            "user": user,
            "action": action,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logs.append(entry)

    def get_user_history(self, user):
        return [log for log in self.logs if log["user"] == user]

    def get_all(self):
        return self.logs
