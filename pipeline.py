import pandas as pd
from src.brand_manufacturer import check_missing_brands_manufacturers
from src.industry_basket_category import check_missing_industry_basket_category
from src.tag_check import check_missing_tags

def run_pipeline(data_file_path, dict_file_path):
    # Read data and dictionary files
    data_df = pd.read_csv(data_file_path)  # Specify the sheet name
    dict_df = pd.read_excel(dict_file_path, sheet_name=None)

    results = {}

    # Check missing brands
    results['Brand'] = check_missing_brands_manufacturers(data_df, dict_df['BrandManufacturer'], 'Brand')

    # Check missing manufacturers
    results['Manufacturer'] = check_missing_brands_manufacturers(data_df, dict_df['BrandManufacturer'], 'Manufacturer')
 
    # Check missing industries
    results['Industry'] = check_missing_industry_basket_category(data_df, dict_df['IndustryBasketCategory'], 'Industry')

    # Check missing baskets
    results['Basket'] = check_missing_industry_basket_category(data_df, dict_df['IndustryBasketCategory'], 'Basket')

    # Check missing categories
    results['Category'] = check_missing_industry_basket_category(data_df, dict_df['IndustryBasketCategory'], 'Category')

    # Check missing tags
    results['Tag'] = check_missing_tags(data_df, dict_df['Tag'])

    return results

def process_and_save_results(results):
    # Filter out empty results
    non_empty_results = {key: value for key, value in results.items() if not value.empty}

    if non_empty_results:
        # Create a DataFrame with separate columns for each category
        results_df = pd.DataFrame(columns=['Brand', 'Manufacturer', 'Industry', 'Basket', 'Category', 'Tag'])

        # Populate the DataFrame with missing elements
        for key, value in non_empty_results.items():
            category_column = key.capitalize()  # Convert key to capitalize for column name
            results_df[category_column] = value

        # Save the DataFrame to a CSV file
        csv_file_path = 'missingdata.csv'
        results_df.to_csv(csv_file_path, index=False)
        print(f"CSV file created with missing data: {csv_file_path}")
    else:
        print("No missing data. CSV file not created.")

# Example usage
#results = run_pipeline(data_file_path, dict_file_path)
#process_and_save_results(results)
