import pandas as pd
import numpy as np


def get_weekly_wage(wage_column):
    """
    Extract the weekly wage from a string.
    
    Parameters:
    wage_str (str): The wage string.
    
    Returns:
    float: The weekly wage as a float.
    """

    new_wage_column = wage_column.str.replace('£', '')
    new_wage_column = new_wage_column.str.replace(',', '')

    new_wage_column = new_wage_column.str.replace('p/w', '')
    new_wage_column = new_wage_column.str.strip()

    # Remove currency symbols and commas, then convert to float
    return new_wage_column.astype(float)

def prepare_fm_data(fm_df):
    """
    
    Prepare the Football Manager data from Medium for analysis.
    Not needed for the ones scraped myself

    """

    fm_df.columns = [x.strip() for x in fm_df.columns]

    for col in fm_df.columns:
        try:
            fm_df[col] = fm_df[col].str.strip()
        except AttributeError:
            continue

    

