import pandas as pd
# Here you can add any global configurations

color_list1 = ["green", "blue"]
color_list2 = ["red", "purple"]
neighbourhood_group = []

data = pd.read_csv("Data/airbnb_open_data_clean.csv")

def get_neighbourhood_groups():
    neighbourhood_group = data['neighbourhood_group'].unique()
    return neighbourhood_group





