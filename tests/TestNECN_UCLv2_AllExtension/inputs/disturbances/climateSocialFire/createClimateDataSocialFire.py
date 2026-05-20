# -*- coding: utf-8 -*-
"""
Created on Fri May  2 13:32:02 2025

@author: Clement + Claude Haiku

Script used to create dummy climate data to test several extensions that
require daily values (BFOLDS Fire, Social Climate Fire) from existing data file
of test files for LANDIS-II extensions.
"""

import os
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

os.chdir(r"D:\OneDrive - UQAM\1 - Projets\Post-Doc - Docker and Apptainer Linux v8\Tool-Docker-Apptainer\Testing_files\TestPnET_AllExtension")

# Step 1: Create date range and empty dataframe
start_date = datetime.date(2000, 1, 1)
end_date = datetime.date(2051, 12, 31)
delta = datetime.timedelta(days=1)

# Create lists to store the date components
dates = []
years = []
months = []
days = []

# Generate all dates
current_date = start_date
while current_date <= end_date:
    dates.append(current_date)
    years.append(current_date.year)
    months.append(current_date.month)
    days.append(current_date.day)
    current_date += delta

# Calculate total number of days
total_days = len(dates)

# Create base dataframe structure
df_columns = ['Year', 'Month', 'Day', 'variable', 'eco1']
df = pd.DataFrame(columns=df_columns)

# Step 2: Process monthly climate data
# Read the monthly climate data
monthly_data = pd.read_csv('./inputs/core/climate.txt', sep='\t')

# Function to get monthly value for a specific variable
def get_monthly_value(year, month, variable):
    # Check if there's a specific entry for the year
    year_match = monthly_data[(monthly_data['Month'] == month) & 
                             (monthly_data['Year'].astype(str).str.contains(str(year)))]

    if not year_match.empty:
        return year_match[variable].values[0]

    # If no specific year entry, use the range data (1999-2300)
    range_match = monthly_data[(monthly_data['Month'] == month) & 
                              (monthly_data['Year'].astype(str).str.contains('1999-2300'))]

    if not range_match.empty:
        return range_match[variable].values[0]

    # Default fallback
    return None

# Step 3: Process daily data
# Read the daily data
daily_data = pd.read_csv('./inputs/disturbances/climateSocialFire/LTB_ClimateInputs_91_10_corrected.csv')

# Filter for years 2000-2007
daily_data_filtered = daily_data[(daily_data['Year'] >= 2000) & (daily_data['Year'] <= 2007)]

# Function to get daily value for a specific variable
def get_daily_value(year, month, day, variable):
    if year <= 2007:
        # For 2000-2007, get actual values
        match = daily_data_filtered[(daily_data_filtered['Year'] == year) & 
                                   (daily_data_filtered['Month'] == month) & 
                                   (daily_data_filtered['Day'] == day) & 
                                   (daily_data_filtered['Variable'] == variable)]
        if not match.empty:
            return match['eco1'].values[0]

    # For 2008-2051, get random values from 2000-2007 for the same month and day
    matches = daily_data_filtered[(daily_data_filtered['Month'] == month) & 
                                 (daily_data_filtered['Day'] == day) & 
                                 (daily_data_filtered['Variable'] == variable)]

    if not matches.empty:
        # Randomly select one value
        return matches.sample(1)['eco1'].values[0]

    # Default fallback
    return None

# Step 4: Fill the dataframe with all variables
# List of variables
monthly_variables = ['Tmax', 'Tmin', 'PAR', 'Prec', 'CO2']
daily_variables = ['maxRH', 'maxtemp', 'minRH', 'mintemp', 'precip', 'winddirection', 'windspeed']

# Create a list to store all rows
all_rows = []

# Process monthly variables
for var in monthly_variables:
    for i in range(total_days):
        year = years[i]
        month = months[i]
        day = days[i]

        # Get the corresponding value from monthly data
        if var == 'Tmax':
            value = get_monthly_value(year, month, 'TMax')
        elif var == 'Tmin':
            value = get_monthly_value(year, month, 'TMin')
        else:
            value = get_monthly_value(year, month, var)

        all_rows.append([year, month, day, var, value])

# Process daily variables
for var in daily_variables:
    for i in range(total_days):
        year = years[i]
        month = months[i]
        day = days[i]

        # Get the corresponding value from daily data
        value = get_daily_value(year, month, day, var)

        all_rows.append([year, month, day, var, value])

# Create the final dataframe
final_df = pd.DataFrame(all_rows, columns=df_columns)

# Step 5: Export to CSV
final_df.to_csv('./inputs/disturbances/climateSocialFire/climate_data_2000_2051.csv', index=False)

print(f"Successfully created dataframe with {len(final_df)} rows and exported to CSV.")
