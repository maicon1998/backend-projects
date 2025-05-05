class Manual:
    manual = """
    # Adding a new task
    task-cli add <description>

    # Updating and deleting tasks
    task-cli update <id> <description>
    task-cli delete <id>

    # Marking a task as in progress or done
    task-cli mark-in-progress <id>
    task-cli mark-done <id>

    # Listing all tasks
    task-cli list

    # Listing tasks by status
    task-cli list done
    task-cli list todo
    task-cli list in-progress"""
