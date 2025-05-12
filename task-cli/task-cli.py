import sys
import datetime

from utils.manual import Manual
from utils.model import Task
from utils.json_manager import Json_manager
from utils.error_messages import valid_args, min_args, valid_status, check_id

from prettytable import PrettyTable

# datetime format
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# load json file
data = Json_manager().load()
tasks = data["tasks"]

match sys.argv[1]:
    # manual
    case "help":
        print(Manual().manual)

    # new task
    case "add":
        # checking for invalid arguments
        min_args(3, "add")

        # id auto increment
        id = max(int(id["id"]) for id in tasks) + 1 if tasks else 0

        new_task = Task(id, sys.argv[2], "todo", current_datetime, current_datetime)
        Json_manager().add(new_task.dictionary())

    # updating tasks
    case "update":
        # checking for invalid arguments
        min_args(4, "update")

        # checking if there is a task with that id
        check = check_id(int(sys.argv[2]), tasks)

        if check:
            Json_manager().update(int(sys.argv[2]), sys.argv[3], current_datetime)
        else:
            sys.exit("No task with this id")

    # deleting tasks
    case "delete":
        # checking for invalid arguments
        valid_args(3, "delete")

        # checking if there is a task with that id
        check = check_id(int(sys.argv[2]), tasks)

        if check:
            Json_manager().delete(int(sys.argv[2]))
        else:
            sys.exit("No task with this id")

    # listing tasks
    case "list":
        if not tasks:
            sys.exit("No tasks")

        table = PrettyTable(tasks[0].keys())

        # listing all tasks
        if len(sys.argv) < 3:
            for item in tasks:
                table.add_row(item.values())

        # list tasks by status
        else:
            # checking for invalid arguments
            valid_args(3, "list-status")
            valid_status(sys.argv[2])

            for item in [item for item in tasks if item["status"] == sys.argv[2]]:
                table.add_row(item.values())

        print(table)

    # uptated the status
    case "mark-in-progress" | "mark-done":
        # checking for invalid arguments
        valid_args(3, "mark")

        # checking if there is a task with that id
        check = check_id(int(sys.argv[2]), tasks)

        if check:
            Json_manager().mark(sys.argv[1], int(sys.argv[2]), current_datetime)
        else:
            sys.exit("No task with this id")

    # invalid arguments
    case _:
        sys.exit("Invalid arguments. Type task-cli help to see the manual")
