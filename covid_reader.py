import pandas as pd


# function that returns common countries in both dataframes
def intersection(lst1, lst2):
    l = [value for value in lst1 if value in lst2]
    return l

# function that returns countries that are not common in the dataframes
def uncommon(lst1, lst2):
    l = [value for value in lst1 if not(value in lst2)]
    return l

# function that prints the countries of both dataframes that have common substring of length > 4
def spell_error_detect(predictor_list, covid_list):
    print(covid_list)
    print(predictor_list)

    for i in predictor_list:
        for j in covid_list:
            answer = longestSubstringFinder(j,i)
            if len(answer) > 4:
                print(i, ':', j)

def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    if len1 > len2:
        len1, len2 = len2, len1
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""
    return answer

# dictionary generated using output of spell_error_detect
country_map = {'brunei darussalam' : 'brunei','czech republic' : 'czechia', 'egypt, arab rep.' : 'egypt',
               'gambia, the' : 'gambia', 'iran, islamic rep.' : 'iran', 'korea, rep.' : 's. korea',
               'kyrgyz republic' : 'kyrgyzstan', 'russian federation' : 'russia',
               'slovak republic' : 'slovakia', 'venezuela, rb' : 'venezuela'}

# retaining only common indexes of covid and predictor dataframe
def df_stanardiser(pred_df, covid_df, country_map):
    # replace the indexes in predictor dataframe with the covid dataframe index value
    pred_indexes = pred_df.index.tolist()
    for key, value in country_map.items():
        idx = pred_indexes.index(key)
        pred_indexes[idx] = value
        pred_df.index = pred_indexes

    index_to_retain = intersection(covid_df.index.tolist(), predictor_df.index.tolist())
    print(index_to_retain, '###################')
    covid_df = covid_df.loc[index_to_retain]
    pred_df = pred_df.loc[index_to_retain]
    return covid_df, pred_df


def preprocess(covid_df, predictor_df):

    # Code for matching indexes of predictor and covid dataframes
    predictor_df.set_index('Country', inplace=True)
    predictor_df.index = predictor_df.index.str.lower()
    covid_df.set_index('country', inplace=True)
    covid_df.index = covid_df.index.str.lower()

    covid_df.dropna(inplace=True, subset=['deaths_per_1M']) # drop rows having na values in the column deaths_per_1M
    #covid_df[['deaths_per_1M']] = covid_df[['deaths_per_1M']].apply(pd.to_numeric)
    #covid_df.apply(pd.to_numeric)

    # the numerical value are stored as strings in the dataframe, with commas
    # Removing comma and converting to numeric value
    covid_df.replace(',', '', regex=True, inplace=True)
    covid_df[covid_df.columns] = covid_df[covid_df.columns].apply(pd.to_numeric, errors='coerce')


    #covid_list = covid_df.index.tolist()
    #predictor_list = predictor_df.index.tolist()
    #spell_error_detect(sorted(uncommon(predictor_list, covid_list)), sorted(uncommon(covid_list, predictor_list)))

    return df_stanardiser(predictor_df, covid_df, country_map)

covid_df = pd.read_csv('./' + 'data/covid_worldometer.csv')
predictor_df = pd.read_csv("./my_df_removedNA.csv")
covid_df, predictor_df = preprocess(covid_df, predictor_df)


'''Replace corrected index in predictor df DONE
    TODO drop uncommon countries from both df DONE
    Clean covid data DONE
'''
