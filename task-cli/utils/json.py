import json


class Json_file:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"tasks": []}

    def dump(self, data, message):
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
            print(message)
        except Exception as e:
            print(f"Error: {e}")
