import pandas as pd


def clean_csv():

    df1 = pd.read_csv('Data/airbnb_open_data.csv', low_memory=False)

    df1 = df1.fillna(0)
    df1.rename(columns=lambda x: (x.replace(' ', '_')).lower(), inplace=True)

    df1['price'] = (df1['price'].replace({'\$': '', ',': ''}, regex=True)).astype(int)
    df1['service_fee'] = (df1['service_fee'].replace({'\$': '', ',': ''}, regex=True)).astype(int)
    df1 = df1.drop(['country', 'country_code'], axis=1)
    df1['last_review'] = pd.to_datetime(df1.last_review)

    df1 = df1.astype({'minimum_nights': int, 'number_of_reviews': int, 'reviews_per_month': int,
                      'review_rate_number': int, 'availability_365': int, 'calculated_host_listings_count': int,
                      'construction_year': int})

    df1.to_csv('Data/airbnb_open_data_clean.csv')


clean_csv()