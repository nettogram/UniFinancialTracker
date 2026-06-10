# Contains functions that pertain to the main function

from rich import print

def list_commands():
    print("\nList of commands: \n")
    print("\t'q' -> quit")
    print("\t'1' -> show total paid for tuition")
    print("\t'2' -> show amount due for the semester")
    print("\t'3' -> show amount due for university years")
    print("\t'4' -> show number of weeks paid")
    print("\t'5' -> add a week of payment")
    print("\t'6' -> show commands")

def add_week(user_info):
    user_info['(D) Times Paid'] += 1
    print(f"\nOne week of pay submitted. Total weeks paid: [yellow]{user_info['Times Paid']}[/yellow]\n") 
    
