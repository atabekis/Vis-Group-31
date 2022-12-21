import pandas as pd
import csv

# Here you can add any global configurations

color_list1 = ["green", "blue"]
color_list2 = ["red", "purple"]
neighbourhood_group = []

data = pd.read_csv("Data/airbnb_open_data_clean.csv")


# returns the neighbourhood groups in the data
def get_neighbourhood_groups():
    neighbourhood_group = data['neighbourhood_group'].unique()
    return neighbourhood_group


# Returns the unique neighbourhoods as items and their groups as keys in a dictionary
def get_neighbourhood():
    neighbourhoods = {'All': list(get_neighbourhood_groups()), 'Manhattan': [], 'Staten Island': [], 'Brooklyn': [],
                      'Bronx': [], 'Queens': []}

    with open("../Data/airbnb_open_data_clean.csv", encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            neighbourhood = line[7]
            group = line[6]

            if (group in neighbourhoods.keys()) and (neighbourhood not in neighbourhoods[group]):
                if neighbourhood != '0':
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
