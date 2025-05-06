import sys
import datetime

from utils.manual import Manual
from utils.model import Task
from utils.json import Json_file
from utils.error_messages import valid_args, min_args, valid_status, check_id

from prettytable import PrettyTable

# datetime format
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# load json file
data = Json_file().load()

match sys.argv[1]:
    # manual
    case "help":
        print(Manual().manual)

    # new task
    case "add":
        min_args(3, "add")

        # id auto increment
        if not data["tasks"]:
            id = 0
        else:
            id = data["tasks"][-1]["id"] + 1

        new_task = Task(id, sys.argv[2], "todo", current_datetime, current_datetime)
        data["tasks"].append(new_task.dictionary())
        Json_file().dump(data, "Added task")

    # updating tasks
    case "update":
        min_args(4, "update")

        task = check_id(int(sys.argv[2]), data["tasks"])

        if task:
            task["description"] = sys.argv[3]
            task["updatedAt"] = current_datetime
            Json_file().dump(data, "Updated task")
        else:
            sys.exit("No task with this id")

    # deleting tasks
    case "delete":
        valid_args(3, "delete")

        check_id = check_id(int(sys.argv[2]), data["tasks"])

        if check_id:
            data["tasks"] = [
                item for item in data["tasks"] if item["id"] != int(sys.argv[2])
            ]
            Json_file().dump(data, "Deleted task")
        else:
            sys.exit("No task with this id")

    # listing all tasks
    case "list":
        if not data["tasks"]:
            sys.exit("No tasks")

        table = PrettyTable(data["tasks"][0].keys())

        if len(sys.argv) < 3:
            for item in data["tasks"]:
                table.add_row(item.values())

        else:
            # list tasks by status
            valid_args(3, "list-status")
            valid_status(sys.argv[2])
            for item in [
                item for item in data["tasks"] if item["status"] == sys.argv[2]
            ]:
                table.add_row(item.values())

        print(table)

    # uptated the status
    case "mark-in-progress" | "mark-done":
        valid_args(3, "mark")

        task = check_id(int(sys.argv[2]), data["tasks"])
        if task:
            task["status"] = sys.argv[1][5:]
            task["updatedAt"] = current_datetime
            Json_file().dump(data, "Updated status")
        else:
            sys.exit("No task with this id")

    # invalid argv
    case _:
        print("Invalid arguments. Type task-cli help to see the manual")
