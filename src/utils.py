import csv
import re  # Import regex for extracting numeric parts
from seating_plan import Guest

def read_input_csv(file_path):
    guests = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract numeric part of guest names
            guest_name = ''.join(filter(str.isdigit, row['Guest']))
            other_guest_name = ''.join(filter(str.isdigit, row['Preference_Guest']))
            preference_score = int(row['Preference_Score'])
            
            if guest_name not in guests:
                guests[guest_name] = Guest(guest_name)
            if other_guest_name not in guests:
                guests[other_guest_name] = Guest(other_guest_name)
            
            guests[guest_name].set_preference(guests[other_guest_name], preference_score)
    
    return list(guests.values())

def write_output_csv(file_path, results):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Algorithm', 'Best_Score', 'Time_Taken', 'Seating_Plan'])
        for result in results:
            writer.writerow(result)