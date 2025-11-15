import os
import pandas as pd
import json

# Set the folder where your data files are located
# Replace this path with the actual folder on your system where the files are
data_folder = r'C:\Users\ub13-glab-015\Desktop\final_lab_exam'

# Change the current working directory to the data folder
os.chdir(data_folder)
print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir())

# File paths (just filenames now because we've changed cwd)
zoo_file = 'zoo.csv'
class_file = 'class.csv'
aux_json_file = 'auxiliary_metadata.json'

# Load CSV files
zoo_df = pd.read_csv(zoo_file)
print("Zoo Data:")
print(zoo_df.head())

class_df = pd.read_csv(class_file)
print("\nClass Data:")
print(class_df.head())

# Load JSON file
with open(aux_json_file, 'r') as f:
    auxiliary_metadata = json.load(f)
print("\nAuxiliary Metadata:")
print(auxiliary_metadata)
 