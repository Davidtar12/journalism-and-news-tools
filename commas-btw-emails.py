import csv

# Replace this with the full path to your CSV file.
csv_file_path = r"C:\Users\david\Downloads\CP\Email lists\abonados,exabonados\audience_export_d0d01fdced (1)\abonados.xlsx"
# List to hold strings from the first column.
first_column_strings = []

# Open and read the CSV file.
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        if row:  # Ensure the row is not empty.
            first_column_strings.append(row[0])

# Join the strings with commas.
result = ",".join(first_column_strings)
print(result)
