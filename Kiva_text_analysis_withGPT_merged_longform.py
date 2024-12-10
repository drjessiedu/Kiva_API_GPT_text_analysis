import pandas as pd

# Step 1: Load the original data from long_form_data.xlsx
long_form_file_path = "long_form_data.xlsx"
long_form_df = pd.read_excel(long_form_file_path)

# Step 2: Load the ratings data from loan_analysis_with_ratings.xlsx
ratings_file_path = "loan_analysis_with_ratings.xlsx"
ratings_df = pd.read_excel(ratings_file_path)

# Step 3: Keep only the LOAN_ID and Concreteness Rating columns in ratings_df
ratings_df = ratings_df[["LOAN_ID", "Concreteness Rating"]]

# Step 4: Merge the Concreteness Rating into the long_form_df based on LOAN_ID
updated_df = long_form_df.merge(ratings_df, on="LOAN_ID", how="left")

# Step 5: Save the updated DataFrame to a new Excel file
output_file_path = "long_form_data_with_ratings.xlsx"
updated_df.to_excel(output_file_path, index=False)

print(f"Updated file saved to {output_file_path}")

