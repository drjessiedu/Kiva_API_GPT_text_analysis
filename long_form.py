#How to transform the kiva data into long form by individual donor's donation amount-Yujia (12/2024).
import pandas as pd
import ast
import os

# File path to the dataset
file_path = 'kiva_2_months.xlsx'

# Ensure the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load the Excel file into a DataFrame
df = pd.read_excel(file_path)

# Create a list to store processed data for each lender
processed_data = []

# Loop through each row in the dataset
for index, row in df.iterrows():
    lenders_data = row['LENDERS']  # Replace with the actual column name for lenders
    other_columns = {  # Collect all other relevant columns in the dataset
        'LENDER_COUNT': row.get('LENDER COUNT'),
        'LENDER_TERM': row.get('LENDER TERM'),
        'REPAYMENT_INTERVAL': row.get('REPAYMENT INTERVAL'),
        'DISTRIBUTION_MODEL': row.get('DISTRIBUTION MODEL'),
        'DISBURSAL_DATE': row.get('DISBURSAL DATE'),
        'USE': row.get('USE'),
        'STATUS': row.get('STATUS'),
        'FUNDED_AMOUNT': row.get('FUNDED AMOUNT'),
        'DATE_RAISED': row.get('DATE RAISED'),
        'PLANNED_EXPIRATION_DATE': row.get('PLANNED EXPIRATION DATE'),
        'FUNDRAISING_DATE': row.get('FUNDRAISING DATE'),
        'LOAN_AMOUNT': row.get('LOAN AMOUNT'),
        'ACTIVITY': row.get('ACTIVITY'),
        'SECTOR': row.get('SECTOR'),
        'DESCRIPTION_ORIGINAL': row.get('DESCRIPTION IN ORIGINAL LANGUAGE'),
        'DESCRIPTION': row.get('DESCRIPTION'),
        'PARTNER_RISK_RATING': row.get('PARTNER RISK RATING'),
        'PARTNER_NAME': row.get('PARTNER NAME'),
        'PARTNER_ID': row.get('PARTNER ID'),
        'ORIGINAL_LANGUAGE': row.get('ORIGINAL_LANGUAGE'),
        'GENDER': row.get('GENDER'),
        'LOAN_COUNTRY': row.get('LOAN COUNTRY'),
        'BORROWER_COUNT': row.get('BORROWER COUNT'),
        'LOAN_NAME': row.get('LOAN_NAME'),
        'LOAN_ID': row.get('LOAN_ID')
    }

    # Parse the LENDERS column
    if isinstance(lenders_data, str):
        try:
            lenders_data = ast.literal_eval(lenders_data)  # Convert string to Python object
        except (ValueError, SyntaxError):
            continue

    # Process each lender in the LENDERS data
    if isinstance(lenders_data, list):
        for lender in lenders_data:
            lender_details = {
                'shareAmount': float(lender['shareAmount']),
                'latestSharePurchaseDate': lender['latestSharePurchaseDate'],
                'id': lender['lender']['id'],
                'publicId': lender['lender']['publicId'],
                'name': lender['lender']['name'],
                'loanCount': lender['lender']['loanCount'],
                'inviteeCount': lender['lender']['inviteeCount'],
                'country': (
                    lender['lender']['lenderPage']['country']['isoCode']
                    if lender['lender']['lenderPage']['country']
                    else 'Unknown'
                ),
                'loanBecause': lender['lender']['lenderPage']['loanBecause'],
                'occupation': lender['lender']['lenderPage']['occupation'],
            }
            # Combine lender details with other row data
            processed_row = {**lender_details, **other_columns}
            processed_data.append(processed_row)

# Convert processed data into a DataFrame
processed_df = pd.DataFrame(processed_data)

# Save the detailed lender contributions to a file
detailed_file_path = 'detailed_lender_contributions.xlsx'
processed_df.to_excel(detailed_file_path, index=False, engine='xlsxwriter')
print(f"Detailed lender contributions saved to {detailed_file_path}")

# Group by lender ID and aggregate the data
grouped_df = processed_df.groupby('id').agg({
    'publicId': 'first',
    'name': 'first',
    'loanCount': 'sum',
    'inviteeCount': 'sum',
    'country': 'first',
    'loanBecause': 'first',
    'occupation': 'first',
    'shareAmount': 'sum',
    'latestSharePurchaseDate': 'max',
    # Aggregating columns from the dataset
    'LENDER_COUNT': 'sum',
    'LENDER_TERM': 'first',
    'REPAYMENT_INTERVAL': 'first',
    'DISTRIBUTION_MODEL': 'first',
    'DISBURSAL_DATE': 'first',
    'USE': 'first',
    'STATUS': 'first',
    'FUNDED_AMOUNT': 'sum',
    'DATE_RAISED': 'first',
    'PLANNED_EXPIRATION_DATE': 'first',
    'FUNDRAISING_DATE': 'first',
    'LOAN_AMOUNT': 'sum',
    'ACTIVITY': 'first',
    'SECTOR': 'first',
    'DESCRIPTION_ORIGINAL': 'first',
    'DESCRIPTION': 'first',
    'PARTNER_RISK_RATING': 'first',
    'PARTNER_NAME': 'first',
    'PARTNER_ID': 'first',
    'ORIGINAL_LANGUAGE': 'first',
    'GENDER': 'first',
    'LOAN_COUNTRY': 'first',
    'BORROWER_COUNT': 'sum',
    'LOAN_NAME': lambda x: ', '.join(set(x)),
    'LOAN_ID': lambda x: ', '.join(map(str, set(x))),
}).reset_index()

# Save the grouped data to a file
grouped_file_path = 'grouped_by_lender_id.xlsx'
grouped_df.to_excel(grouped_file_path, index=False, engine='xlsxwriter')
print(f"Grouped data saved to {grouped_file_path}")
