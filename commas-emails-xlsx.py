import pandas as pd

# Replace with the full path to your Excel file.
excel_file_path = r"C:\Users\USERNAME\Downloads\CP\Email lists\abonados,exabonados\audience_export_d0d01fdced (1)\abonados.xlsx"

# Read the Excel file (by default, reads the first sheet)
df = pd.read_excel(excel_file_path)

# Convert the first column to a list of strings.
first_column_strings = df.iloc[:, 0].astype(str).tolist()

# Join the strings with commas.
result = ",".join(first_column_strings)
print(result)

