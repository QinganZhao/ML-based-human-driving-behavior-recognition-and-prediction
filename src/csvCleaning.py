import pandas as pd
import os

# change the working directory
os.chdir('/Users/franklin/Desktop')

# change the file name
df = pd.read_csv('pcap1.csv')

df['Feature'] = df['Feature'].str.replace('(', '')
df['Feature'] = df['Feature'].str.replace(')', '')
df[['Feature1', 'Feature2', 'Feature3', 'Feature4', 'Feature5']] = df['Feature'].str.split(',',expand=True)
df.drop('Unnamed: 0', axis=1, inplace=True)
df.drop('Feature', axis=1, inplace=True)

# change the path and name of the output csv
df.to_csv('pcap1out_new.csv')
