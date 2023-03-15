import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read in the data
df = pd.read_csv('session_results.csv')

df = df.groupby('FullName').filter(lambda x: len(x) >= 5)

# if Time is NaN, set it to 0

# df['Time'] = df['Time'].fillna(0)

# create a new column called Year and set it to the year of the EventDate

df['Year'] = pd.DatetimeIndex(df['EventDate']).year

# Filter out any drivers that do not appear in all the unique years in the dataset

df = df.groupby('FullName').filter(lambda x: len(x['Year'].unique()) == len(df['Year'].unique()))

# Count how many races each driver has participated in
driver_counts = df['FullName'].value_counts()

# Print this as a dataframe with driver with the most races at the top
print(driver_counts.to_frame().head())

# Define the weights for each unlucky event
unlucky_events = {
    'Engine': -10,
    'Transmission': -8,
    'Collision damage': -9,
    'Power Unit': -9,
    'Gearbox': -7,
    'Hydraulics': -4,
    'Suspension': -5,
    'Electronics': -6,
    'Fuel leak': -4,
    'Water leak': -5,
    'Turbo': -3,
    'Fuel pump': -4,
    'Exhaust': -5,
    'Overheating': -5,
    'Differential': -5,
    'Radiator': -5,
    'Puncture': -5,
    'Undertray': -5,
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
    'Vibrations': -5,
    'Wheel': -6,
    'Debris': -5,
    'Fuel pressure': -3
}

# Create a dictionary to store each driver's weighted score and number of races completed
driver_scores = {}
driver_races = {}

# Iterate through each row of the data and calculate the weighted score and number of races for each driver
for index, row in df.iterrows():
    driver = row['FullName']
    status = row['Status']
    if status in unlucky_events:
        score = unlucky_events.get(status, 0)
        driver_scores[driver] = driver_scores.get(driver, 0) + score
    driver_races[driver] = driver_races.get(driver, 0) + 1

# Convert the dictionaries to pandas dataframes
scores_df = pd.DataFrame.from_dict(driver_scores, orient='index', columns=['Score'])
races_df = pd.DataFrame.from_dict(driver_races, orient='index', columns=['Races'])

# Combine the dataframes and calculate the weighted score per race for each driver
combined_df = pd.concat([scores_df, races_df], axis=1)
combined_df['Weighted Score'] = combined_df['Score'] / combined_df['Races']

# Calculate mean and standard deviation of weighted scores
mean_score = combined_df['Weighted Score'].mean()
std_score = combined_df['Weighted Score'].std()

# Calculate the z-scores for each driver's weighted score
combined_df['Z-Score'] = (combined_df['Weighted Score'] - combined_df['Weighted Score'].mean()) / combined_df['Weighted Score'].std()

# Sort the dataframe by z-score
combined_df = combined_df.sort_values(by='Z-Score', ascending=False)

#crate a color map where the lower the z-score, the more unlucky the driver and the more red the color

cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Plot the results using a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(combined_df[['Weighted Score']], center=0, annot=True, fmt='.2f', linewidths=.5, cmap=cmap)
plt.title('Weighted Scores per Race for Unlucky Drivers')
plt.xlabel('Driver')
plt.ylabel('Score')
plt.show()

# Create a heatmap with the driver names in the middle of the bars
fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(combined_df[['Weighted Score']],
            annot=True, fmt='.2f', cmap='RdYlGn',
            linewidths=.5, square=True, ax=ax,
            cbar_kws={'label': 'Unlucky Drivers'},
            annot_kws={'fontsize': 7})
ax.set_title('Unlucky Drivers', fontsize=14, fontweight='bold')
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
plt.savefig('UnluckyDrivers.png')

# Display the heatmap
plt.show()
