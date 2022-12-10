import pandas as pd
# Here you can add any global configurations

color_list1 = ["green", "blue"]
color_list2 = ["red", "purple"]
neighbourhood_group = []

data = pd.read_csv("Data/airbnb_open_data_clean.csv")

#returns the neighbourhood groups in the data
def get_neighbourhood_groups():
    neighbourhood_group = data['neighbourhood_group'].unique()
    return neighbourhood_group

#returns the maximum and the minimum price in the data
def get_price_min_max():
    max = data['price'].max()
    min = data['price'].min()
    return int(min), int(max)

#returns the possible values of instant bookability
def get_inst_bookable():
    bookable = data['instant_bookable'].unique()
    return bookable




