# Financial stats calculator, for budgeting

weekly_pay = 450
times_paid = 17
weekly_tuition_pay = 275
weekly_family_pay = 175
semester_cost = 4500
semester_count = 6

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

while True:
    selection = input("Select an option by typing a command: ")
    
    if selection == 'q':
        break
    elif selection == '1':
        print(f"\nTotal paid for so far: ${current_amount_paid}\n") 
    elif selection == '2':
        print(f"\nTotal amount due for semester: ${semester_amount_due}\n") 
    elif selection == '3':
        print(f"\nAmount due for university: ${total_amount_due}\n") 
    else:
        print("\nInvalid command.\n")


