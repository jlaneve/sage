import csv

# Open the input files
with open('all.cm', 'r') as cm_file, open('all.nl', 'r') as nl_file:
    # Read the lines from each file
    cm_lines = cm_file.readlines()
    nl_lines = nl_file.readlines()

# Create a list of tuples with corresponding lines
lines = zip(nl_lines, cm_lines)

# Write the lines into a CSV file
with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['nl', 'cm'])  # Write the header
    writer.writerows(lines)  # Write the lines