import sys


def valid_args(len_valid_args, error_msg):
    if len(sys.argv) == len_valid_args:
        pass

    else:
        match error_msg:
            case "delete":
                return sys.exit("Invalid arguments. Usage: task-cli delete <id>")

            case "mark":
                return sys.exit(
                    "Invalid arguments. Usage: task-cli <mark-in-progress> <id> or <mark-done> <id>"
                )

            case "list":
                return sys.exit("Invalid arguments. Usage: task-cli list")

            case "list-status":
                return sys.exit(
                    "Invalid arguments. Usage: task-cli list <done> or <todo> or <in-progress>"
                )


def min_args(len_min_args, error_msg):
    if len(sys.argv) != len_min_args:
        match error_msg:
            case "add":
                return sys.exit(
                    "Invalid arguments. Usage: task-cli add <'description'>"
                )
            case "update":
                return sys.exit(
                    "Invalid arguments. Usage: task-cli update <id> <description>"
                )


def valid_status(status):
    if status not in ["done", "todo", "in-progress"]:
        return sys.exit(
            "Invalid arguments. Usage: task-cli list <done> or <todo> or <in-progress>"
        )


def check_id(id, data):
    return next((item for item in data if item["id"] == id), None)
