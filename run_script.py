from src.pipeline import run_pipeline

data_file_path = 'UIM_data.csv'
dict_file_path = 'UIM_dictionary.xlsx'

results = run_pipeline(data_file_path, dict_file_path)

# Process the results as needed
for key, result in results.items():
    print(f"\nResults for {key}:\n{result}")
