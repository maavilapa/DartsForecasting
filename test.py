import pandas as pd
#importing the os module
import os

#to get the current working directory
directory = os.getcwd()

print(directory)
pd.read_csv(directory + "\DartsForecasting\historical_data.csv")
