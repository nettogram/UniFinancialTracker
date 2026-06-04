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

weekly_pay = user_info['Weekly Pay']
times_paid = user_info['Times Paid']
weekly_tuition_pay = user_info['Weekly Tuition Pay']
weekly_family_pay = user_info['Weekly Family Pay']
semester_cost = user_info['Semester Cost']
semester_count = user_info['Current Semester Count']

total_cost = semester_cost * semester_count
current_total_tuition_pay = weekly_tuition_pay * times_paid

semester_counter = int((weekly_tuition_pay * times_paid) / semester_cost)

current_amount_paid = weekly_tuition_pay * times_paid
semester_amount_due = (semester_cost * (semester_counter + 1)) - (current_amount_paid)
total_amount_due = total_cost - current_amount_paid

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
        print(f"\nTotal paid for so far: ${current_amount_paid}\n") 
    elif selection == '2':
        print(f"\nTotal amount due for semester: ${semester_amount_due}\n") 
    elif selection == '3':
        print(f"\nAmount due for university: ${total_amount_due}\n") 
    elif selection == '4':
        print(f"\nTotal weeks of payment: {times_paid}\n") 
    elif selection == '5':
        times_paid += 1
        user_info['Times Paid'] = times_paid
        print(f"\nOne week of pay submitted. Total weeks paid: {times_paid}\n") 
    else:
        print("\nInvalid command.\n")


