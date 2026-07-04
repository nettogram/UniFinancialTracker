# Financial stats calculator, for budgeting

from rich import print

from datafunctions import add_week, list_commands
from saveload import load_stats, refreshstats, save_stats

savefile = "saves/savefiletest.json"  # currently testing new saves feature


def main():
    user_info = load_stats(savefile)
    current_stats = refreshstats(user_info)

    list_commands()

    while True:
        selection = input("\nSelect an option by typing a command: ")

        if selection == "q":
            save_stats(savefile, user_info)
            print("\n[italic]Program exiting.[/italic]")
            break
        elif selection == "1":
            print(
                f"\nTotal paid for so far: [yellow]${current_stats['Tuition Paid']}[/yellow]\n"
            )
        elif selection == "2":
            print(
                f"\nTotal amount due for semester: [red]${current_stats['Semester Amount Due']}[/red]\n"
            )
        elif selection == "3":
            print(
                f"\nAmount due for university: [red]${current_stats['Total Amount Due']}[/red]\n"
            )
        elif selection == "4":
            print(
                f"\nTotal weeks of payment: [green]{current_stats['Times Paid']}[/green]\n"
            )
        elif selection == "5":
            add_week(user_info, current_stats)
            current_stats = refreshstats(user_info)
        elif selection == "6":
            list_commands()
        else:
            print("\n[italic red]Invalid command.[/italic red]\n")


if __name__ == "__main__":
    main()
