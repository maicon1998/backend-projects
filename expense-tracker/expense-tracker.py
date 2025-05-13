import argparse
import datetime

from prettytable import PrettyTable

from utils.csv_manager import Csv_manager


parser = argparse.ArgumentParser(description="Expenser tracker")
subparsers = parser.add_subparsers(dest="command", help="Available commands")

# add an expense
add_parser = subparsers.add_parser("add", help="add an expense")
add_parser.add_argument(
    "--description", type=str, required=True, help="description of the expense"
)
add_parser.add_argument(
    "--amount", type=float, required=True, help="amount of the expense"
)

# update an expense
update_parser = subparsers.add_parser("update", help="update an expense")
update_parser.add_argument(
    "--id", type=int, required=True, help="expense you want to update"
)
update_parser.add_argument(
    "--description",
    type=str,
    required=True,
    help="update the description of the expense",
)
update_parser.add_argument(
    "--amount", type=float, required=True, help="update the amount of the expense"
)

# delete an expense
delete_parser = subparsers.add_parser("delete", help="delete an expense")
delete_parser.add_argument(
    "--id", type=int, required=True, help="expense you want to delete"
)

# list
list_parser = subparsers.add_parser("list", help="list all expenses")

# summary
summary_parser = subparsers.add_parser("summary", help="summary of expenses")
summary_parser.add_argument(
    "--month", type=int, help="summary of expenses for a specific month"
)

args = parser.parse_args()

match args.command:
    case "add":
        data = Csv_manager().reader()

        id = max(int(id["id"]) for id in data) + 1 if data else 0

        row = {
            "id": id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "description": args.description,
            "amount": args.amount,
        }

        Csv_manager().add(row)

        print("Added expense")

    case "update":
        Csv_manager().update(args.id, args.description, args.amount)
        print("Updated expense")

    case "delete":
        Csv_manager().delete(args.id)
        print("Deleted expense")

    case "list":
        if not Csv_manager().reader():
            print("No expenses")

        else:
            table = PrettyTable(Csv_manager().reader()[0].keys())
            for row in Csv_manager().reader():
                table.add_row(row.values())

            print(table)

    case "summary":
        if args.month:
            month_sum = sum(
                float(row["amount"])
                for row in Csv_manager().reader()
                if datetime.datetime.strptime(row["date"], "%Y-%m-%d").month
                == args.month
            )

            print(f"${month_sum}")

        else:
            summary = sum(float(row["amount"]) for row in Csv_manager().reader())
            print(f"${summary}")
