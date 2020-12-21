import pandas as pd

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def preprocess_covid(covid_df):
    predictor_df = pd.read_csv("./my_df_removedNA.csv")
    predictor_df.set_index('Country', inplace=True)
    predictor_df.index = predictor_df.index.str.lower()

    covid_df.set_index('country', inplace=True)
    covid_df.index = covid_df.index.str.lower()

    covid_list = covid_df.index.tolist()
    predictor_list = predictor_df.index.tolist()


    print(covid_list)
    print(predictor_list)

    print(len(intersection(covid_list, predictor_list)))
    print(len(intersection(predictor_list, covid_list)))



covid_df = pd.read_csv('./' + 'data/covid_worldometer.csv')
preprocess_covid(covid_df)
