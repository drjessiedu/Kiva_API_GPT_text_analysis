#This code use GPT to run text analysis. Change api key and data file name if needed.- Yujia (12/2024)
from openai import OpenAI

client = OpenAI(api_key="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")
import pandas as pd
import time

# Load your Excel file
file_path = "kiva_2_months.xlsx"  # Replace with your file path
sheet_name = "Sheet2"  # Replace with the correct sheet name if applicable

# Load data into DataFrame
df = pd.read_excel(file_path,sheet_name)

# Column containing descriptions
description_column = "DESCRIPTION"  # Replace with the correct column name
df["Concreteness Rating"] = None  # Add a new column for GPT responses

# OpenAI API key
  # Replace with your OpenAI API key

# Define the prompt
base_prompt = (
    "You are a smart research assistant. You will analyze descriptions of loan usage from Kiva.org, "
    "a platform that provides small loans to individual borrowers or small businesses. These descriptions were framed in different types of languages. "
    "Some words are more concrete and some are more abstract. Concrete words are those related to direct experience, such as verbs that describe an observable action "
    "and nouns that describe an observable object. Concrete words are relatively verifiable and provide contextualized specificity. Abstract words, in contrast, "
    "are more situationally invariant, such as adjectives and verbs that describe an enduring state and nouns that describe a concept or idea that applies across varying contexts. "
    'For example, "to buy 50 trousers and 30 shirts" is more concrete, while "to finance clean energy products to thousands of households in South Africa" is more abstract '
    'because the words “trousers”, “shirts”, and the number “50” or “30” are more concrete than the words “products” or “thousands of”.\n\n'
    "Your task is to rate each loan description on a scale of 1 to 7, where 1 means 'very concrete' and 7 means 'very abstract'. "
    "The descriptions will be provided in a Python list. Please respond with only a single number for each description. Do not explain yourself.\n\n"
)

# Process rows in batches to avoid exceeding API limits
batch_size = 100  # Adjust batch size based on your needs
for idx, row in df.iterrows():
    try:
        description = row[description_column]

        # Construct the full prompt for each description
        prompts = f"{base_prompt}- {description}\n"

        # Send request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompts},
            ],
        temperature=0.2)

        # Extract the rating (response content)
        rating = response.choices[0].message.content.strip()
        df.at[idx, "Concreteness Rating"] = rating

        print(f"Processed row {idx + 1}/{len(df)}: Rating = {rating}")

        # Throttle to respect rate limits
        time.sleep(2)  # Adjust delay as per rate limits
    except Exception as e:
        print(f"Error processing row {idx}: {e}")
        continue
    
# Save the results back to Excel
output_file = "loan_analysis_with_ratings.xlsx"  # Define your output file name
df.to_excel(output_file, index=False)
print(f"Analysis completed. Results saved to {output_file}.")
