# -*- coding: utf-8 -*-
"""
Created on Fri May  2 13:32:02 2025

@author: Clement + Claude Haiku

Script used to create dummy Spin up climate data to test several extensions that
require daily values (BFOLDS Fire, Social Climate Fire) from existing data file
of test files for LANDIS-II extensions.

Is based on the climate data created by createClimateDataSocialFire.py.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

os.chdir(r"D:\OneDrive - UQAM\1 - Projets\Post-Doc - Docker and Apptainer Linux v8\Tool-Docker-Apptainer\Testing_files\TestPnET_AllExtension")

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('./inputs/disturbances/climateSocialFire/climate_data_2000_2051.csv')

# Convert date columns to datetime
df['date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

# Get all unique variables
variables = df['variable'].unique()

# Create a date range from 1900-01-01 to 2000-01-01
start_date = pd.Timestamp('1900-01-01')
end_date = pd.Timestamp('2000-12-31')
date_range = pd.date_range(start=start_date, end=end_date)

# Create a new DataFrame with one row per day for each variable
new_rows = []
for var in variables:
    for date in date_range:
        new_rows.append({
            'Year': date.year,
            'Month': date.month,
            'Day': date.day,
            'variable': var,
            'date': date,
            'eco1': None  # Will be filled with averages
        })

new_df = pd.DataFrame(new_rows)

# For each day in the new DataFrame, calculate the average value from the original DataFrame
# for the same month and day across all years from 2000 to 2051
for var in variables:
    for month in range(1, 13):
        for day in range(1, 32):
            # Skip invalid dates
            try:
                datetime(2000, month, day)
            except ValueError:
                continue

            # Filter original data for this variable, month, and day
            mask = (df['variable'] == var) & (df['Month'] == month) & (df['Day'] == day)
            if not df[mask].empty:
                avg_value = df[mask]['eco1'].mean()

                # Apply this average to all matching days in the new DataFrame
                new_mask = (new_df['variable'] == var) & (new_df['Month'] == month) & (new_df['Day'] == day)
                new_df.loc[new_mask, 'eco1'] = avg_value

# Drop the temporary 'date' column if not needed
new_df = new_df.drop('date', axis=1)

# Save the result to a new CSV file
new_df.to_csv('./inputs/disturbances/climateSocialFire/climate_data_spinUp_1900_2000.csv', index=False)

print("Processing complete. Results saved to 'historical_averages.csv'")
