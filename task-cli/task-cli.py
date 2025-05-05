import sys
import datetime

from utils.manual import Manual
from utils.model import Task
from utils.json import Json_file
from utils.error_messages import Msg

from prettytable import PrettyTable

# datetime format
datetime = datetime.datetime.now().strftime(
    f"{'%Y'}-{'%m'}-{'%d'} {'%H'}:{'%M'}:{'%S'}"
)

# load json file
data = Json_file().load()

# manual
if sys.argv[1] == "help":
    print(Manual().manual)

# new task
elif sys.argv[1] == "add":
    if len(sys.argv) == 3:
        # id auto increment
        if not data["tasks"]:
            id = 0
        else:
            id = data["tasks"][-1]["id"] + 1

        new_task = Task(id, sys.argv[2], "todo", datetime, datetime)
        data["tasks"].append(new_task.dictionary())
        Json_file().dump(data, "Added task")

    # missing task description
    elif len(sys.argv) == 2:
        sys.exit(Msg.missing_description)

    # more than 3 argv
    else:
        sys.exit(Msg.exceeded)

# updating tasks
elif sys.argv[1] == "update":
    if len(sys.argv) == 4:
        for item in data["tasks"]:
            if item["id"] == int(sys.argv[2]):
                item["description"] = sys.argv[3]
                item["updatedAt"] = datetime
                break

        Json_file().dump(data, "Updated task")

    # missing task id
    elif len(sys.argv) == 2:
        sys.exit(Msg.missing_id)

    # missing task description
    elif len(sys.argv) == 3:
        sys.exit("Msg.missing_description")

    # more than 4 args
    else:
        sys.exit(Msg.exceeded)

# deleting tasks
elif sys.argv[1] == "delete":
    if len(sys.argv) == 3:
        data["tasks"] = [
            item for item in data["tasks"] if item["id"] != int(sys.argv[2])
        ]
        Json_file().dump(data, "Deleted task")

    # missing task id
    elif len(sys.argv) == 2:
        sys.exit(Msg.missing_id)

    # more than 3 argv
    else:
        sys.exit(Msg.exceeded)

# listing all tasks
elif sys.argv[1] == "list":
    table = PrettyTable(data["tasks"][0].keys())

    if len(sys.argv) < 3:
        for item in data["tasks"]:
            table.add_row(item.values())
        print(table)

    # invalid status
    elif sys.argv[2] not in ["done", "todo", "in-progress"]:
        sys.exit("Invalid argument. Options: done, todo, in-progress")

    # list tasks by status
    else:
        for item in data["tasks"]:
            if item["status"] == sys.argv[2]:
                for item in data["tasks"]:
                    table.add_row(item.values())

# uptated the status
elif sys.argv[1] in ["mark-in-progress", "mark-done"]:
    if len(sys.argv) == 3:
        for item in data["tasks"]:
            if item["id"] == int(sys.argv[2]):
                item["status"] = sys.argv[1][5:]
                item["updatedAt"] = datetime
                break
        Json_file().dump(data, "Updated status")

    else:
        # more than 3 argv
        sys.exit(Msg.exceeded)

# invalid argv
else:
    sys.exit(Msg.invalid)
