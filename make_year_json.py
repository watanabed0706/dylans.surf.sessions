import calendar
import json
import sys

YEAR = int(sys.argv[1])
OUTPUT = sys.argv[2]

# Make Dictionary of Specified Year
def generate_month_json(year):
    month_data = {}
    for month_index in range(1, 13):
        month_name = calendar.month_name[month_index]
        _, num_days = calendar.monthrange(year, month_index)
        month_data[month_name] = [0.0 for _ in range(num_days)]
    return month_data

month_dict = generate_month_json(YEAR)

# Dump Dictionary into YYYY.json
with open(OUTPUT, "w") as f:
    json.dump(month_dict, f, indent=4)