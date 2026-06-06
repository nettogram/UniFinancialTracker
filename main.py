# Financial stats calculator, for budgeting
import json
from rich import print

savefile = 'saves/savefile.json'
try:
    with open(savefile) as saves:
        user_info = json.load(saves)
except FileNotFoundError:
    user_info = {

        'Weekly Pay': 450,
        'Times Paid': 0,
        'Weekly Tuition Pay': 275,
        'Weekly Family Pay': 175,
        'Semester Cost': 4500,
        'Current Semester Count': 6
    }
    with open(savefile, 'w') as saves:
        json.dump(user_info, saves)
    print("\n[italic green]Basic save contents initialized.[/italic green]")
    user_info['Times Paid'] = int(input("Please enter current amount of times paid: "))
else:
    print("\n[italic green]Save contents loaded.[/italic green]")

def refresh_stats(user_info):

    """ Refreshes data when information is added/changed"""
    # temporary local variables - for calculation
    total_cost = user_info['Semester Cost'] * user_info['Current Semester Count']
    tuition_paid = user_info['Weekly Tuition Pay'] * user_info['Times Paid']
    semester_counter = int((user_info['Weekly Tuition Pay'] * user_info['Times Paid']) / user_info['Semester Cost'])
    semester_amount_due = (user_info['Semester Cost'] * (semester_counter + 1)) - tuition_paid
    total_amount_due = total_cost - tuition_paid

    refreshed_stats = {
        'Total Cost' : total_cost,
        'Tuition Paid' : tuition_paid,
        'Semester Counter' : semester_counter,
        'Semester Amount Due' : semester_amount_due, 
        'Total Amount Due' : total_amount_due
    }
    
    return refreshed_stats

def list_commands():
    print("\nList of commands: \n")
    print("\t'q' -> quit")
    print("\t'1' -> show total paid for tuition")
    print("\t'2' -> show amount due for the semester")
    print("\t'3' -> show amount due for university years")
    print("\t'4' -> show number of weeks paid")
    print("\t'5' -> add a week of payment")
    print("\t'6' -> show commands")

current_stats = refresh_stats(user_info)

list_commands()

while True:
    selection = input("\nSelect an option by typing a command: ")
    
    if selection == 'q':
        with open(savefile, 'w') as newsave:
            user_info = json.dump(user_info, newsave)
        print("\n[italic]Program exiting.[/italic]")
        break
    elif selection == '1':
        print(f"\nTotal paid for so far: [yellow]${current_stats['Tuition Paid']}[/yellow]\n") 
    elif selection == '2':
        print(f"\nTotal amount due for semester: [red]${current_stats['Semester Amount Due']}[/red]\n") 
    elif selection == '3':
        print(f"\nAmount due for university: [red]${current_stats['Total Amount Due']}[/red]\n") 
    elif selection == '4':
        print(f"\nTotal weeks of payment: [green]{user_info['Times Paid']}[/green]\n") 
    elif selection == '5':
        user_info['Times Paid'] += 1
        current_stats = refresh_stats(user_info)
        print(f"\nOne week of pay submitted. Total weeks paid: [yellow]{user_info['Times Paid']}[/yellow]\n") 
    elif selection == '6':
        list_commands()
    else:
        print("\n[italic red]Invalid command.[/italic red]\n")



