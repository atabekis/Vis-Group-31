import pandas as pd
import csv
import numpy as np
from collections import Counter


# Global configurations
neighbourhood_group = []

#Data read from clean dataset generated from clean.py
data = pd.read_csv("Data/airbnb_open_data_clean.csv", low_memory=False)

# returns the neighbourhood groups in the data
def get_neighbourhood_groups():
    #get all unique values
    neighbourhood_group = data['neighbourhood_group'].unique()
    neighbourhood_group = list(neighbourhood_group)
    #disregards values that might be data artifacts
    try:
        neighbourhood_group.remove(np.nan)
        neighbourhood_group.remove('Brookln')
        neighbourhood_group.remove('Manhatan')
    except:
        print("Exception occurred")

    #add the option "All" in the list for filtering possiblities
    neighbourhood_group = np.insert(neighbourhood_group, 0, "All")
    return neighbourhood_group

# Returns the unique neighbourhoods as items and their groups as keys in a dictionary
# for future reference to neighbourhood groups and what neighbourhoods they contain
def get_neighbourhood():
    neighbourhoods = {'All': [], 'Manhattan': [], 'Staten Island': [], 'Brooklyn': [],
                      'Bronx': [], 'Queens': []}

    # add All as an option to all neighbourhoods
    for key in neighbourhoods:
        neighbourhoods[key].append("All")

    with open("./data/airbnb_open_data_clean.csv", encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            #get the neighbourhoodgood and the corresponding neighbourhood from columns 5 and 6 of the data
            neighbourhood = line[5]
            group = line[4]

            if (group in neighbourhoods.keys()) and (neighbourhood not in neighbourhoods[group]):
                if neighbourhood != '0':
                    neighbourhoods['All'].append(neighbourhood)
                    neighbourhoods[group].append(neighbourhood)
    return neighbourhoods


# returns the maximum and the minimum price in the data
def get_price_min_max():
    max = data['price'].max()
    min = data['price'].min()
    return int(min), int(max)

# returns the maximum and the minimum service fee price
def get_service_fee():
    max = data['service_fee'].max()
    min = data['service_fee'].min()
    return int(min), int(max)

# Counts the amount of words in the "processed" column of a given dataframe such that it returns a dataframe which contains word-count tuple
# Params:
#   df: Datagrame with processed words as a column
#   count: the amount of words that will be returned in the dataframe
def count_words(df, count):
    #get the processed words as a list
    processed_words = df['processed'].to_list()

    #clean the processed words from white space and add in a new list
    clean = []
    for word in processed_words:
        if type(word) == str:
            clean += (word.split(' '))

    clean = [i for i in clean if len(i) > 2]
    #count the ocurrence of every word
    amounts = Counter(clean).most_common(count)

    return pd.DataFrame(amounts, columns=['word', 'count'])