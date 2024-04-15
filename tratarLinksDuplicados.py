import pandas as pd

# Read the Excel file
file_path = 'airbnb_links.xlsx'
df = pd.read_excel(file_path)

# Remove duplicate values from the "Link" column
df = df.drop_duplicates(subset=['Link'])

# Save the modified DataFrame back to the Excel file
df.to_excel(file_path, index=False)

print("Duplicates removed and file updated successfully.")
