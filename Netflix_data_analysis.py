# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('Netflix_data.csv', encoding_errors='ignore', engine='python')

# -----------------------------
# Basic Data Cleaning
# -----------------------------

# Remove rows with missing values
df.dropna(inplace=True)

# Convert Vote_Average column to float
df['Vote_Average'] = df['Vote_Average'].astype('float')

# Convert Release_Date to datetime format
df['Release_Date'] = pd.to_datetime(df['Release_Date'])

# Extract only year from Release_Date
df['Release_Date'] = df['Release_Date'].dt.year
print(df['Release_Date'].dtype)

# Rename column for better readability
df.rename(columns={'Release_Date': 'Release_Year'}, inplace=True)

# Drop unnecessary columns
df.drop(columns=['Overview', 'Original_Language', 'Poster_Url'], axis=1, inplace=True)


# -----------------------------
# Categorizing Vote Average
# -----------------------------

def categorize_col(df, cols, labels):
    """
    Categorize a numerical column into bins based on
    min, 25%, 50%, 75%, and max values.
    """
    edges = [
        df[cols].describe()['min'],
        df[cols].describe()['25%'],
        df[cols].describe()['50%'],
        df[cols].describe()['75%'],
        df[cols].describe()['max']
    ]
    
    df[cols] = pd.cut(df[cols], edges, labels=labels, duplicates='drop')
    return df


# Labels for categorization
labels = ['Not_popular', 'Below_avg', 'Average', 'Popular']

# Apply categorization
categorize_col(df, 'Vote_Average', labels)

# Remove any new missing values after categorization
df.dropna(inplace=True)


# -----------------------------
# Genre Column Processing
# -----------------------------

# Split multiple genres into list
df['Genre'] = df['Genre'].str.split(', ')

# Convert each genre into separate rows
df = df.explode('Genre').reset_index(drop=True)

# Convert Genre column to categorical type
df['Genre'] = df['Genre'].astype('category')


# -----------------------------
# Visualization Section
# -----------------------------

# Distribution of movies released per year
plt.figure(figsize=(10, 5))

a = sns.histplot(x='Release_Year', binwidth=10, data=df)

# Add labels on bars
for bars in a.containers:
    a.bar_label(bars)

plt.title("Release Year Distribution")
plt.xlabel("Release Year")
plt.ylabel("Number of Movies")

plt.show()
