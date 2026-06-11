# Contains functions that pertain to the main function

from rich import print
from datetime import date, timedelta
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

def add_week(user_info, current_stats):
    last_pay_date = date.fromisoformat(user_info["Dates Of Pay"][-1])
    date_today = date.today()
    
    if last_pay_date.weekday() >= 3:
        next_avaliable_pay_day = 7 - (last_pay_date.weekday() - 3)
        next_avaliable_pay_date = date(date_today.year, date_today.month, (last_pay_date.day + next_avaliable_pay_day))
    else: 
        next_avaliable_pay_day = 3 - last_pay_date.weekday()
        next_avaliable_pay_date = date(date_today.year, date_today.month, (last_pay_date.day + next_avaliable_pay_day))

    if date_today.weekday() >= 3:
        current_next_avaliable_pay_day = 7 - (date_today.weekday() - 3) 
    else:
        current_next_avaliable_pay_day = 3 - date_today.weekday()   

    if date_today >= next_avaliable_pay_date:
        user_info['(D) Times Paid'] += 1
        user_info['Dates Of Pay'].append(date_today.isoformat())
        current_stats = refreshstats(user_info)
        print(f"\nOne pay entry submitted. Total weeks paid: [yellow]{current_stats['Times Paid']}[/yellow]\n") 

    else: 
        print(f"\n[red]Error: Last pay entry date was {last_pay_date}. You must wait {current_next_avaliable_pay_day} day(s) before the next payment.[/red]\n")

    return current_stats
    
