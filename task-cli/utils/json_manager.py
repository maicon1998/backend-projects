import json


class Json_manager:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"tasks": []}

    def dump(self, data):
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error: {e}")

    def add(self, data):
        try:
            load = self.load()
            load["tasks"].append(data)
            self.dump(load)
            print("Added Task")
        except Exception as e:
            print(f"Error when adding: {e}")

    def update(self, id, description, current_datetime):
        try:
            data = self.load()
            for item in data["tasks"]:
                if item["id"] == id:
                    item["description"] = description
                    item["updatedAt"] = current_datetime
                self.dump(data)
            print("Updated task")
        except Exception as e:
            print(f"Error when updating: {e}")

    def delete(self, id):
        try:
            data = self.load()
            data["tasks"] = [item for item in data["tasks"] if item["id"] != id]
            self.dump(data)
            print("Deleted task")
        except Exception as e:
            print(f"Error when deleting: {e}")

    def mark(self, status, id, current_datetime):
        try:
            data = self.load()
            for item in data["tasks"]:
                if item["id"] == id:
                    item["status"] = status[5:]
                    item["updatedAt"] = current_datetime
                self.dump(data)
            print("Updated status")
        except Exception as e:
            print(f"Error updating status: {e}")
