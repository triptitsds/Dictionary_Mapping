import pandas as pd

def check_missing_industry_basket_category(data_df, dict_df, column_name):
    unique_brands = data_df[column_name].unique()
    missing_brands = [brand for brand in unique_brands if brand not in dict_df[column_name].values]
    return pd.DataFrame({'Missing {}'.format(column_name): missing_brands})
