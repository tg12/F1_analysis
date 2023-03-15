# Define rating for each status
status_rating = {'Finished': 10,
                 '+1 Lap': -1,
                 'Retired': -10,
                 '+2 Laps': -2,
                 'Transmission': -8,
                 'Engine': -10,
                 'Accident': -9,
                 'Gearbox': -7,
                 'Brakes': -6,
                 'Hydraulics': -4,
                 'Collision damage': -9,
                 'Water leak': -5,
                 'Fuel leak': -4,
                 'Spun off': -7,
                 'Suspension': -5,
                 'Electronics': -6,
                 'Wheel': -6,
                 'Fuel pressure': -3,
                 'Overheating': -5,
                 'Collision': -8,
                 'Turbo': -3,
                 'Vibrations': -5,
                 'Power Unit': -9,
                 'Debris': -5,
                 'Exhaust': -5,
                 'Fuel pump': -4,
                 '+3 Laps': -3,
                 'Differential': -5,
                 'Radiator': -5,
                 'Puncture': -5,
                 'Illness': 0,
                 'Water pressure': -5,
                 '+6 Laps': -6,
                 'Undertray': -5,
                 '+5 Laps': -5,
                 'Disqualified': -10,
                 'Oil leak': -4,
                 'Front wing': -5,
                 'Wheel nut': -4,
                 'Driveshaft': -6,
                 'Mechanical': -7,
                 'Damage': -8,
                 'Cooling system': -5,
                 'Water pump': -5,
                 'Electrical': -6,
                 'Power loss': -7,
                 'Withdrew': -9,
                 'Rear wing': -5}

import pandas as pd
import numpy as np
from scipy.stats import norm

# Read in dataset
df = pd.read_csv('session_results.csv')

# remove any rows where the FullName count is less than 5 across the entire dataset

df = df.groupby('FullName').filter(lambda x: len(x) >= 5)

# Drop Q1, Q2, and Q3 columns
df = df.drop(['Q1', 'Q2', 'Q3'], axis=1)

# Convert time to seconds
df['Seconds'] = pd.to_timedelta(df['Time']).dt.total_seconds()

# Calculate improvement score for each driver
first_half = df[df['Seconds'] < df['Seconds'].median()]
second_half = df[df['Seconds'] >= df['Seconds'].median()]

# Calculate mean and standard deviation of position for each driver in the first half
first_half_means = first_half.groupby('FullName')['Position'].mean()
first_half_stdevs = first_half.groupby('FullName')['Position'].std()

# Calculate Z-scores for each driver's position in each race in the second half
second_half_zscores = (second_half.groupby(['FullName', 'BroadcastName'], group_keys=True)['Position']
                       .apply(lambda x: (x - first_half_means[x.name[0]]) / first_half_stdevs[x.name[0]]))

# Ignore drivers with less than 5 races
driver_counts = second_half.groupby('FullName').size()
valid_drivers = driver_counts[driver_counts >= 5].index.tolist()
second_half_zscores = second_half_zscores[second_half_zscores.index.get_level_values('FullName').isin(valid_drivers)]

# Calculate the improvement score for each driver
improvement_scores = ((second_half_zscores.groupby('FullName').mean() - 
                      second_half_zscores.groupby('FullName').std()) * 
                     (1 - norm.cdf(second_half_zscores.groupby('FullName').mean())))

# Create DataFrame of drivers and their improvement scores
results_df = pd.DataFrame({'FullName': improvement_scores.index.tolist(),
                           'ImprovementScore': improvement_scores.tolist()})

# Sort DataFrame by improvement score
results_df = results_df.sort_values('ImprovementScore', ascending=False)

# Print DataFrame
print(results_df)



