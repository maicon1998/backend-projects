import csv


class Csv_manager:
    def __init__(self, filename="data.csv"):
        self.filename = filename

    def reader(self):
        try:
            with open(self.filename, "r") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            return []

    def write_rows(self, rows):
        with open(self.filename, "w", newline="") as file:
            csv_writer = csv.DictWriter(
                file, fieldnames=["id", "date", "description", "amount"], delimiter=","
            )
            csv_writer.writeheader()
            csv_writer.writerows(rows)

    def add(self, row):
        try:
            data = self.reader()
            data.append(row)
            self.write_rows(data)
        except Exception as e:
            print(f"Error when adding: {e}")

    def update(self, id, description, amount):
        try:
            data = self.reader()
            for row in data:
                if row["id"] == str(id):
                    row["description"] = description
                    row["amount"] = amount
                self.write_rows(data)
        except Exception as e:
            print(f"Error when updating: {e}")

    def delete(self, id):
        try:
            delete = (row for row in self.reader() if row["id"] != str(id))
            self.write_rows(delete)
        except Exception as e:
            print(f"Error when deleting {e}")
