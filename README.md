# f1_data_analysis

f1_data_analysis is a github repository dedicated to analyzing data from the world of Formula 1 racing. 

Python Code for Analyzing Formula 1 Session Results

This Python code analyzes data related to Formula 1 racing. It uses the following libraries to read in, clean, process, and visualize F1 session results data:

Pandas
Seaborn
Matplotlib

## The driver_luck_score performs the following tasks:

Reads in a CSV file containing F1 session results.

Filters out any drivers that have not participated in at least five races.

Creates a new column called ‘Year’ and sets it to the year of the EventDate column.

Filters out any drivers that do not appear in all the unique years in the dataset.

Counts how many races each driver has participated in and prints this as a dataframe with the driver with the most races at the top.

Defines a dictionary containing weights for each unlucky event such as engine failure or collision damage.

Iterates through each row of the data and calculates the weighted score and number of races for each driver.

Converts the results to pandas dataframes, combines them, and calculates the weighted score per race for each driver.

Calculates the mean and standard deviation of weighted scores and z-scores for each driver’s weighted score.

Sorts the dataframe by z-score.

Uses Seaborn and Matplotlib to create heatmaps visualizing the results.

Creates a heatmap with the driver names in the middle of the bars and a color map where the lower the z-score, the more unlucky the driver and the more red the color.

Saves the heatmap as an image and displays it.

## The driver improvement score (v2)

This Python code analyzes data related to Formula 1 racing results. It starts by defining a dictionary called status_rating which assigns a numerical rating to each status, representing how good or bad it is for a driver's performance. The code then uses Pandas, Numpy, and Scipy libraries to read in and process the data, and calculate a driver's improvement score based on their performance in the second half of the race compared to the first half.

The code reads in a CSV file containing F1 session results and filters out any drivers that have not participated in at least five races. It drops the Qualifying columns and converts the Time column to seconds. It then calculates the improvement score for each driver using the following steps:

Divides the race results into two halves, the first half and the second half.

Calculates the mean and standard deviation of position for each driver in the first half.

Calculates the Z-scores for each driver's position in each race in the second half, using the mean and standard deviation from the first half.
Ignores drivers with less than 5 races.

Calculates the improvement score for each driver using the formula: (Z-score mean - Z-score standard deviation) * (1 - normal cumulative distribution function (CDF) of Z-score mean).

The code creates a DataFrame of drivers and their improvement scores and sorts it by the improvement score in descending order. Finally, the code prints the DataFrame, which shows each driver's improvement score based on their performance in the second half of the race compared to the first half.

## The driver improvement score. 

This code is performing an analysis on a dataset of Formula 1 race results to calculate the improvement score for each driver. The improvement score is a combination of two metrics: position change and weighted points.

Here's what the code is doing step by step:

Define a dictionary that assigns a rating to each possible status that a driver can finish a race with.

Read in the race results data from a CSV file and filter out any drivers who have competed in less than 5 races.

Create a new column in the DataFrame called "Year" and set it to the year of the race.

Filter out any drivers who have not competed in all the unique years in the dataset.

Drop columns that are not needed for the analysis.

Calculate the improvement score for each driver by taking the median of their position change and weighted points, normalizing the two metrics, and then combining them with equal weight.

Sort the drivers by their improvement score and display the results in a table using the tabulate library.

Plot the improvement scores for each driver as a horizontal bar chart.

Create a heatmap of the improvement scores using the seaborn library, with the driver names in the middle of the bars.

Save the heatmap as a PNG file and display it.

You can also follow me on Twitter at to stay up-to-date on the latest developments.

[Twitter!]( https://twitter.com/James12396379)

We are passionate about this project and would love your support. If you're feeling generous and want to keep me motivated, consider buying us a cold one! Your contribution means the world to me and will help us continue this important work.

[Paypal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=EV8XUGXX76UXQ&source=url)

### BTC Address: 3QjWqhQbHdHgWeYHTpmorP8Pe1wgDjJy54

### ETH Address: 0x01d23570c34A78380452A4BE9C95bAe439719bAf
