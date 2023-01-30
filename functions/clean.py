import json
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk.data
from nltk.stem import WordNetLemmatizer
import re
import numpy as np

#create the NTA column in the data
def create_nta(df):
    with open('./data/neighbourhoods.geojson') as f:
        neighbourhoods = json.load(f)

    ntas = []

    for i in neighbourhoods['features']:
        ntas.append(i['properties']['ntaname'])

    df['NTA'] = 'None'

    for index, row in df.iterrows():
        neighbourhood = row['neighbourhood']
        for nta in ntas:
            if str(neighbourhood) in nta:
                # print(neighbourhood, nta)
                df.at[index, 'NTA'] = nta
                break
        if df.at[index, 'NTA'] == 'None':
            df.at[index, 'NTA'] = neighbourhood

    return df

#process the descriptions of the listings to create descriptive words specific to each listing
def preprocess(text, banned):
    lemmatize = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    letters_only = re.sub("[^a-zA-Z]", " ", text).lower()
    word_tokens = word_tokenize(letters_only)

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    clean_words = []

    for word in filtered_sentence:
        if word not in banned:
            clean_words.append(lemmatize.lemmatize(word))

    return " ".join(clean_words)

#add the preprocessed text to the data
def get_keywords(dataframe):
    # Check whether nltk has the required packages
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    try:
        nltk.data.find('tokenizers/punkt/english.pickle')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/wordnet.zip/wordnet/')
    except LookupError:
        nltk.download('wordnet')
        nltk.download('omw-1.4')

    data_filtered = dataframe[['id', 'name']]
    data_filtered = data_filtered.astype({'name': 'string'})
    neig1 = list(dataframe['neighbourhood'].unique())
    neig2 = list(dataframe['neighbourhood_group'].unique())

    remove_words = neig1 + neig2

    remove_words = [str(x).lower() for x in remove_words if (x != 0)]

    dataframe['processed'] = data_filtered.apply(lambda x: preprocess(text=x['name'], banned=remove_words), axis=1)

    return dataframe

#clean the data from redundant data that will not be used
def clean_csv():
    print('Cleaning the dataset...')

    df1 = pd.read_csv('./data/airbnb_open_data.csv', low_memory=False)

    #fill na values with 0
    df1 = df1.fillna(0)
    #rename columns
    df1.rename(columns=lambda x: (x.replace(' ', '_')).lower(), inplace=True)

    #set the type of price values
    df1['price'] = (df1['price'].replace({'\$': '', ',': ''}, regex=True)).astype(int)
    #drop the rows that have no price (equal to 0) since these can cause errors in processing
    df1 = df1[df1["price"] != 0]

    #set the type of service fee
    df1['service_fee'] = (df1['service_fee'].replace({'\$': '', ',': ''}, regex=True)).astype(int)
    #drop the country codes since all data is within US
    df1 = df1.drop(['country', 'country_code'], axis=1)
    #set date and time to correct format
    df1['last_review'] = pd.to_datetime(df1.last_review)

    #set the types of columns
    df1 = df1.astype({'minimum_nights': int, 'number_of_reviews': int, 'reviews_per_month': int,
                      'review_rate_number': int, 'availability_365': int, 'calculated_host_listings_count': int,
                      'construction_year': int, 'instant_bookable' : str})

    #capitalise neighbourhood group names
    df1['neighbourhood_group'] = df1['neighbourhood_group'].str.title()
    #replace nan values with None
    df1['neighbourhood_group'] = df1['neighbourhood_group'].replace(np.nan, 'None')

    #fill in the missing neighbourhood and group names by backtracking the whole dataset
    for index, row in df1.iterrows():
        neighbourhood, group = row['neighbourhood'], row['neighbourhood_group']
        if group == 'None':
            group_new = (df1[df1['neighbourhood'] == neighbourhood].iloc[7]['neighbourhood_group'])
            df1.at[index, 'neighbourhood_group'] = group_new
        elif neighbourhood == "None":
            neighbourhood_new = (df1[df1['neighbourhood_group'] == group].iloc[7]['neighbourhood'])
            df1.at[index, 'neighbourhood'] = neighbourhood_new
        elif group == "Brookln":
            df1.at[index, 'neighbourhood_group'] = "Brooklyn"
        elif group == "Manhatan":
            df1.at[index, 'neighbourhood_group'] = "Manhattan"

    #drop columns that will not be needed
    df1 = df1.drop(columns=['host_id', 'host_name', 'license'])

    #replace instant bookable nan values with default "TRUE"
    df1['instant_bookable'] = df1['instant_bookable'].replace("0", "True")

    #drop rows that do not have lat and long values
    df1 = df1[df1['lat'] != 0]
    df1 = df1[df1['lat'] != 0]

    #Fill rules
    df1['house_rules'] = df1['house_rules'].replace(0, 'No rules provided')
    #Fill name
    df1['name'] = df1['name'].replace(0, "No name Provided")
    #Fill host identity
    df1['host_identity_verified'] = df1['host_identity_verified'].replace(0, 'unconfirmed')
    #fill cancellation policy
    df1['cancellation_policy'] = df1['cancellation_policy'].replace(0, 'Not Specified')


    print('Preprocessing the text...')

    df_processed = get_keywords(df1)

    print('Creating the neighbourhood geolocations...')

    df_nta = create_nta(df_processed)

    df_nta.to_csv('./data/airbnb_open_data_clean.csv')


clean_csv()
