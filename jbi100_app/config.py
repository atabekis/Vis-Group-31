import pandas as pd
import csv

import numpy as np

# Here you can add any global configurations

color_list1 = ["green", "blue"]
color_list2 = ["red", "purple"]
neighbourhood_group = []

data = pd.read_csv("Data/airbnb_open_data_clean.csv")


# returns the neighbourhood groups in the data
def get_neighbourhood_groups():
    neighbourhood_group = data['neighbourhood_group'].unique()
    neighbourhood_group = np.insert(neighbourhood_group, 0 , "All")
    return neighbourhood_group


# Returns the unique neighbourhoods as items and their groups as keys in a dictionary
def get_neighbourhood():
    neighbourhoods = {'All': [], 'Manhattan': [], 'Staten Island': [], 'Brooklyn': [],
                      'Bronx': [], 'Queens': []}

    #add All as an option to all neighbourhoods
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
    return bookable
