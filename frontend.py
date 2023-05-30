# libraries
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb

from IPython.display import display
from numpy import where
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report, confusion_matrix, multilabel_confusion_matrix
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures, StandardScaler
from sklearn.svm import OneClassSVM


# Constants
TRAINING_YEAR = 2015
TESTING_YEAR = 2017
ATTRIBUTE_SIZE = 6

def linear_model():
    # We might not need player_data.csv and players.csv since they are personal information that we can not make use of
    salary_20 = pd.read_csv("salary_0020.csv")
    salary_17 = pd.read_csv("salary_1718.csv")
    stats = pd.read_csv("1950/seasons_stats.csv")
    stats = stats.drop(stats.columns[0], axis=1)
    pd.set_option('display.max_columns', None)

    team_names = {
        "Atlanta Hawks":"ATL",
        "Boston Celtics":"BOS",
        "Brooklyn Nets":"BKN",
        "Charlotte Hornets":"CHA",
        "Charlotte Bobcats":"CHB",
        "Chicago Bulls":"CHI",
        "Cleveland Cavaliers":"CLE",
        "Dallas Mavericks":"DAL",
        "Denver Nuggets":"DEN",
        "Detroit Pistons":"DET",
        "Golden State Warriors":"GSW",
        "Houston Rockets":"HOU",
        "Indiana Pacers":"IND",
        "LA Clippers":"LAC",
        "Los Angeles Clippers": "LAC",
        "Los Angeles Lakers":"LAL",
        "Memphis Grizzlies":"MEM",
        "Miami Heat":"MIA",
        "Milwaukee Bucks":"MIL",
        "Minnesota Timberwolves":"MIN",
        "New Orleans Pelicans":"NOP",
        "New York Knicks":"NYK",
        "Oklahoma City Thunder":"OKC",
        "Orlando Magic":"ORL",
        "Philadelphia 76ers":"PHI",
        "Phoenix Suns":"PHX",
        "Portland Trail Blazers":"POR",
        "Sacramento Kings":"SAC",
        "San Antonio Spurs":"SAS",
        "Toronto Raptors":"TOR",
        "Utah Jazz":"UTA",
        "Washington Wizards":"WAS",
        "Seattle SuperSonics":"SEA",
        "Vancouver Grizzlies":"VAN",
        "New Jersey Nets":"NJN",
        "New Orleans Hornets":"NOK",
    }

    unknowns = [
        'Madrid Real Madrid',
        "null Unknown",
        "NO/Oklahoma City Hornets",
        'Bilbao Basket Bilbao Basket',
        "Fenerbahce Ulker Fenerbahce Ulker",
        "Maccabi Haifa Maccabi Haifa"
    ]

    # Convert team names in 0020 dataset to abbreviations
    for i in range(len(salary_20)):
        v = salary_20['team'][i]
        if v in unknowns:
            continue
        salary_20.loc[i,'team'] = team_names[v]

    # Remove unknowns
    for v in unknowns:
        salary_20 = salary_20[salary_20['team'] != v]

    # Only use players from 2000 onward
    stats = stats[stats['Year'] >= 2000]

    # Add salary to stats dataset based on player, year
    merged_00_to_17 = stats.merge(salary_20, left_on=['Year', 'Player', 'Tm'], right_on=['season', 'name', 'team'])

    # Drop unused columns that we think are irrelevant from merged dataset
    merged_00_to_17 = merged_00_to_17.drop(columns = ['Player', 'Pos', 'Tm', '3PAr', 'blanl', 'blank2', 'rank', 'position', 'team', 'name', 'season'])

    # Replace Nan with 0
    merged_00_to_17.fillna(0, inplace=True)

    # Different datasets to see what produces best predictions
    # Can either always predict later year or split train, test throughout years

    merged_10_to_17 = merged_00_to_17[merged_00_to_17['Year'] >= 2010]

    merged_13_to_17 = merged_00_to_17[merged_00_to_17['Year'] >= 2013]

    # Using 16 to predict 17

    merged_16_17 = merged_00_to_17[merged_00_to_17['Year'] >= 2016]

    # Split within year

    merged_17 = merged_00_to_17[merged_00_to_17['Year'] >= 2017]

    # Filter the most relevant attributes
    filtered_0017 =  merged_00_to_17.drop(['Year'], axis=1)

    # Only need the salary column, and take out the correlation with salary itself
    correlation = abs(filtered_0017.corr()['salary'][:-1])

    # Get the sorted index of correlation
    attribute_rank = np.argsort(correlation)

    # Get the most relevant attributes
    relevant_attributes = attribute_rank.index[attribute_rank[-ATTRIBUTE_SIZE:]]

    # Filter out some outliers in order to make better predictions
    data = merged_00_to_17[merged_00_to_17['Year'] == TRAINING_YEAR]
    data = data.drop(['Year'], axis=1)

    # Max is usually calculated by Q3 + 1.5 * IQR, where IQR = Q3 - Q1
    q3, q1 = np.quantile(data['salary'], [0.75, 0.25])
    local_max = q3 + 1.5 * (q3 - q1)

    data = data.reset_index(drop=True)
    sb.boxplot(data['salary'])

    # Get rid of outliers
    data = data[data['salary'] <= local_max]

    # Split the data
    df_salary = data.copy()
    salary_train, salary_test = train_test_split(df_salary, test_size=0.2)
    X_salary_train, y_salary_train = salary_train[relevant_attributes], salary_train['salary']

    # Scale the data, but keep the original salary because we need to get the actual prediction
    scaler = StandardScaler()
    scaler.fit(X_salary_train)

    Z_salary_train = scaler.transform(X_salary_train)

    # Training the linear regression model 
    poly = PolynomialFeatures(degree = 1, include_bias = False)
    x_poly_train = poly.fit_transform(Z_salary_train)

    model = LinearRegression().fit(x_poly_train, y_salary_train)

    return scaler, model

if __name__ == '__main__':
    scaler, model = linear_model()

    while True:
        # Get input from front-end
        attributes = None

        data = scaler.transform(attributes)
        prediction = model.predict(data)
