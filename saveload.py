# Contains functions for save and load states
import json

from rich import print


def load_stats(savefile):
    try:
        with open(savefile) as saves:
            user_info = json.load(saves)
    except FileNotFoundError:
        user_info = {  # Basic emergency JSON template
            "Weekly Pay": 450,
            "(ND) Times Paid": 20,
            "Dates Of Pay": [
                "2026-06-04",
                "2026-11-04",
            ],
            "(D) Times Paid": 0,
            "Weekly Tuition Pay": 275,
            "Weekly Family Pay": 175,
            "Semester Cost": 4500,
            "Current Semester Count": 6,
        }
        with open(savefile, "w") as saves:
            json.dump(user_info, saves)
        print("\n[italic green]Basic save contents initialized.[/italic green]")
        user_info["(D) Times Paid"] = int(
            input("Please enter current amount of times paid: ")
        )
        return user_info
    else:
        print("\n[italic green]Save contents loaded.[/italic green]")
        return user_info


def refreshstats(user_info):
    """Local data refresh when information is added/changed"""

    # local calculations to change data
    total_cost = user_info["Semester Cost"] * user_info["Current Semester Count"]
    times_paid = user_info["(ND) Times Paid"] + user_info["(D) Times Paid"]
    tuition_paid = user_info["Weekly Tuition Pay"] * times_paid
    total_amount_due = total_cost - tuition_paid
    semester_counter = int(
        ((user_info["Weekly Tuition Pay"]) * times_paid) / user_info["Semester Cost"]
    )
    semester_amount_due = (
        user_info["Semester Cost"] * (semester_counter + 1)
    ) - tuition_paid
    current_semester_paid = user_info["Semester Cost"] - semester_amount_due
    semester_pay_remaining = round(semester_amount_due / user_info["Weekly Tuition Pay"])

    # takes local calculations and edits information local to app runtime
    refreshed_stats = {
        "Total Cost": total_cost,
        "Tuition Paid": tuition_paid,
        "Semester Counter": semester_counter,
        "Semester Amount Due": semester_amount_due,
        "Total Amount Due": total_amount_due,
        "Times Paid": times_paid,
        "Current Semester Paid": current_semester_paid,
        "Semester Pay Remaining": semester_pay_remaining,
    }

    return refreshed_stats


def save_stats(savefile, user_info):
    """Saves all data (including edited) back into JSON"""
    with open(savefile, "w") as newsave:
        user_info = json.dump(user_info, newsave)
