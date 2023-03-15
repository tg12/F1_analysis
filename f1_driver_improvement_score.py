
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


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Read in dataset and filter drivers with less than 5 races
df = pd.read_csv('session_results.csv')
df = df.groupby('FullName').filter(lambda x: len(x) >= 5)

# if Time is NaN, set it to 0

# df['Time'] = df['Time'].fillna(0)

# create a new column called Year and set it to the year of the EventDate

df['Year'] = pd.DatetimeIndex(df['EventDate']).year

# Filter out any drivers that do not appear in all the unique years in the dataset

df = df.groupby('FullName').filter(lambda x: len(x['Year'].unique()) == len(df['Year'].unique()))



# Drop irrelevant columns
df = df.drop(['Q1', 'Q2', 'Q3'], axis=1)

# Calculate improvement score based on position change and weighted points
df['WeightedPoints'] = df['Status'].map(status_rating) * df['Points']
df['PositionChange'] = (1 / np.log(df['Position'] + 2)) * (df['GridPosition'] - df['Position'])

driver_stats = df.groupby(['FullName']).agg({'PositionChange': 'median', 'WeightedPoints': 'median'})
driver_counts = df.groupby('FullName').size()
valid_drivers = driver_counts[driver_counts >= 5].index.tolist()
driver_stats = driver_stats[driver_stats.index.isin(valid_drivers)]

mean_pc, std_pc = np.mean(driver_stats['PositionChange']), np.std(driver_stats['PositionChange'])
mean_wp, std_wp = np.mean(driver_stats['WeightedPoints']), np.std(driver_stats['WeightedPoints'])

driver_stats['PositionChange'] = (driver_stats['PositionChange'] - mean_pc) / std_pc
driver_stats['WeightedPoints'] = (driver_stats['WeightedPoints'] - mean_wp) / std_wp

driver_stats['ImprovementScore'] = 0.5 * driver_stats['PositionChange'] + 0.5 * driver_stats['WeightedPoints']
driver_stats = driver_stats.sort_values(by=['ImprovementScore'], ascending=False)

# Print results in a table using tabulate
from tabulate import tabulate

print(tabulate(driver_stats, headers='keys', tablefmt='psql'))

# Plot results as a bar chart and a heatmap using matplotlib and seaborn
plt.figure(figsize=(10, 10))
plt.barh(driver_stats.index, driver_stats['ImprovementScore'], color=driver_stats['ImprovementScore'].apply(lambda x: 'g' if x > 0 else 'r'))
plt.title('Improvement Score')
plt.xlabel('Improvement Score')
plt.ylabel('Driver')
plt.show()

# Create a heatmap with the driver names in the middle of the bars
fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(driver_stats[['ImprovementScore']],
            annot=True, fmt='.2f', cmap='RdYlGn',
            linewidths=.5, square=True, ax=ax,
            cbar_kws={'label': 'Improvement Score'},
            annot_kws={'fontsize': 7})
ax.set_title('Driver Improvement Score', fontsize=14, fontweight='bold')
ax.set_ylabel('Driver', fontsize=12)

# Rotate the x and y labels
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

# Set the font sizes for the x and y tick labels
plt.tick_params(axis='both', which='major', labelsize=8)

# Set the x-axis label position to bottom
ax.xaxis.set_label_position('bottom')

# Add padding to the left and bottom of the heatmap
plt.subplots_adjust(left=0.3, bottom=0.25)

# Save the figure
plt.savefig('improvement_score.png')

# Display the heatmap
plt.show()
