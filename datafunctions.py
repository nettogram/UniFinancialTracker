# Contains functions that pertain to the main function

from datetime import date, timedelta

from rich import print

from saveload import refreshstats


def list_commands():
    print("\nList of commands: \n")
    print("\t'q' -> quit")
    print("\t'1' -> show total paid for tuition")
    print("\t'2' -> show amount due for the semester")
    print("\t'3' -> show amount due for university years")
    print("\t'4' -> show number of weeks paid")
    print("\t'5' -> add a week of payment")
    print("\t'6' -> show commands")

# Adds week of pay when button is pressed
def add_week(user_info, current_stats):
    last_pay_date = date.fromisoformat(user_info["Dates Of Pay"][-1])
    date_today = date.today()
    entry_status = "NULL"

    # Calculates to the next thursday from the last pay (algorithm)
    if last_pay_date.weekday() >= 3:
        next_avaliable_pay_day = 7 - (last_pay_date.weekday() - 3)
    else:
        next_avaliable_pay_day = 3 - last_pay_date.weekday()

    # timedelta calculates the next pay date from the previous calculation
    # considering month skips, etc...
    next_avaliable_pay_date = last_pay_date + timedelta(days=next_avaliable_pay_day)

    if date_today >= next_avaliable_pay_date:
        # Edits Global info
        user_info["(D) Times Paid"] += 1
        user_info["Dates Of Pay"].append(date_today.isoformat())

        # refreshes stats for UI
        current_stats = refreshstats(user_info)
        
        # Status flag for a successful addition
        entry_status = "OK"
        current_stats["Entry Status"] = entry_status
        print(
            f"\nOne pay entry submitted. Total weeks paid: [yellow]{current_stats['Times Paid']}[/yellow]\n"
        )
        return current_stats

    else:
        # Legacy CLI output for unsuccessful pay log
        print(
            f"\n[red]Error: Last pay entry date was {last_pay_date}. You must wait {next_avaliable_pay_day} day(s) before the next payment.[/red]\n"
        )
        
        # status flag for unsuccessful addition 
        entry_status = "FAIL"
        current_stats["Entry Status"] = entry_status
        return current_stats
