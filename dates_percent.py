import os
from datetime import datetime
import server_info

def calc_percent():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    start_date = datetime(2024, 1, 19)  # For example, January 1st, 2024
    end_date = datetime(2024, 8, 1)    # For example, December 31st, 2024

    # Get the current date
    current_date = datetime.now()

    # Calculate the total days between the start and end dates
    total_days = (end_date - start_date).days

    # Calculate the number of days elapsed between the start date and the current date
    elapsed_days = (current_date - start_date).days

    # Calculate the percentage progress
    progress_percentage = (elapsed_days / total_days) * 100
    progress_percentage_formatted = "{:.2f}".format(progress_percentage)
    server_info.set_data("progress_date", progress_percentage, ROOT_DIR)
    print("Progress percentage:", progress_percentage_formatted)