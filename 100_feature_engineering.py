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


