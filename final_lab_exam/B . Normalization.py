import pandas as pd
import numpy as np
import os

# Print title and gap for clarity
print("\n" * 3)
print("E. Handle Missing Values Based on Roll Number Second to Last Digit")
print("-" * 70)
print("\n")

# Set working directory and load merged data CSV
data_folder = r'C:\Users\ub13-glab-015\Desktop\final_lab_exam'
os.chdir(data_folder)

merged_file = 'merged_zoo_aux.csv'  # Output from previous merge step
merged_df = pd.read_csv(merged_file)

print("Loaded merged dataset sample:")
print(merged_df.head())

# Extract the second last digit from roll number string for deciding strategy
roll_number = "24UG00312"  # Replace with your actual roll number
second_last_digit = int(roll_number[-2])

print(f"\nRoll number: {roll_number}")
print(f"Second to last digit: {second_last_digit}")

# Define missing value handling functions based on your digit

def handle_missing(df, digit):
    df = df.copy()
    if digit in [0,1,2]:
        # Strategy 1: Fill missing numeric cols with mean, categorical with mode
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                mean_val = df[col].mean()
                df[col].fillna(mean_val, inplace=True)
            else:
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col].fillna(mode_val[0], inplace=True)
    elif digit in [3,4,5]:
        # Strategy 2: Fill all missing values with zero or 'Unknown' for strings
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col].fillna(0, inplace=True)
            else:
                df[col].fillna('Unknown', inplace=True)
    elif digit in [6,7,8,9]:
        # Strategy 3: Drop all rows with any missing values
        df = df.dropna()
    else:
        print("Digit outside expected range, no missing value handling applied.")
    return df

# Apply missing value handling 
final_df = handle_missing(merged_df, second_last_digit)

print("\nDataset sample after handling missing values:")
print(final_df.head())

# Save the final cleaned file
output_file = 'merged_zoo_aux_missing_handled.csv'
final_df.to_csv(output_file, index=False)
print(f"\nFinal dataset with missing values handled saved to '{output_file}'.")
