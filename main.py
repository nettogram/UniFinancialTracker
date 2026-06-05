# Financial stats calculator, for budgeting
import json

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
    print("Basic save contents initialized.\n")
    user_info['Times Paid'] = int(input("Please enter current amount of times paid: "))
else:
    print("Save contents loaded.\n")

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

current_stats = refresh_stats(user_info)

print("List of commands: ")
print("'q' -> quit")
print("'1' -> show total paid for tuition")
print("'2' -> show amount due for the semester")
print("'3' -> show amount due for university years")
print("'4' -> show number of weeks paid")
print("'5' -> add a week of payment")

while True:
    selection = input("Select an option by typing a command: ")
    
    if selection == 'q':
        with open(savefile, 'w') as newsave:
            user_info = json.dump(user_info, newsave)
        print("Entries saved. Program exiting.")
        break
    elif selection == '1':
        print(f"\nTotal paid for so far: ${current_stats['Tuition Paid']}\n") 
    elif selection == '2':
        print(f"\nTotal amount due for semester: ${current_stats['Semester Amount Due']}\n") 
    elif selection == '3':
        print(f"\nAmount due for university: ${current_stats['Total Amount Due']}\n") 
    elif selection == '4':
        print(f"\nTotal weeks of payment: {user_info['Times Paid']}\n") 
    elif selection == '5':
        user_info['Times Paid'] += 1
        current_stats = refresh_stats(user_info)
        print(f"\nOne week of pay submitted. Total weeks paid: {user_info['Times Paid']}\n") 
    else:
        print("\nInvalid command.\n")


