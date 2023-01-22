import re
import pandas as pd
import csv
import numpy as np
from collections import Counter
import json




# Here you can add any global configurations

color_list1 = ["green", "blue"]
color_list2 = ["red", "purple"]
neighbourhood_group = []

data = pd.read_csv("Data/airbnb_open_data_clean.csv", low_memory=False)


# returns the neighbourhood groups in the data
def get_neighbourhood_groups():
    neighbourhood_group = data['neighbourhood_group'].unique()
    neighbourhood_group = list(neighbourhood_group)
    neighbourhood_group.remove(np.nan)
    neighbourhood_group.remove('Brookln')
    neighbourhood_group.remove('Manhatan')
    neighbourhood_group = np.insert(neighbourhood_group, 0, "All")
    return neighbourhood_group


# Returns the unique neighbourhoods as items and their groups as keys in a dictionary
def get_neighbourhood():
    neighbourhoods = {'All': [], 'Manhattan': [], 'Staten Island': [], 'Brooklyn': [],
                      'Bronx': [], 'Queens': []}

    # add All as an option to all neighbourhoods
    for key in neighbourhoods:
        neighbourhoods[key].append("All")

    with open("Data/airbnb_open_data_clean.csv", encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            neighbourhood = line[7]
            group = line[6]

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


# returns the possible values of instant bookability
def get_inst_bookable():
    bookable = data['instant_bookable'].unique()
    bookable = list(bookable)
    bookable.remove('0')
    return bookable


def get_service_fee():
    max = data['service_fee'].max()
    min = data['service_fee'].min()
    return int(min), int(max)


def count_words(df, count):
    
    processed_words = df['processed'].to_list()
    clean = []
    for word in processed_words:
        if type(word) == str:
            clean += (word.split(' '))

    clean = [i for i in clean if len(i) > 2]
    amounts = Counter(clean).most_common(count)

    return pd.DataFrame(amounts, columns=['word', 'count'])