import pandas as pd

csv_dir = './intermediate_results/'
data_dir = './data/'

# function that returns common countries in both dataframes
def intersection(lst1, lst2):
    l = [value for value in lst1 if value in lst2]
    return l

# function that returns countries that are not common in the dataframes
def uncommon(lst1, lst2):
    l = [value for value in lst1 if not(value in lst2)]
    return l

# function that prints the countries of both dataframes that have common substring of length > 4
# Some countries have different names (Different cases, short form names) in the indexes
def spell_error_detect(predictor_list, covid_list):
    print('List of country names represented differently in predictor data and COVID data, respectively')
    for i in predictor_list:
        for j in covid_list:
            answer = longestSubstringFinder(j,i)
            if len(answer) > 4:
                print(i, ':', j, end=', ')

# function implementing longest common substring problem
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

# dictionary generated using output of spell_error_detect()
country_map = {'brunei darussalam' : 'brunei','czech republic' : 'czechia', 'egypt, arab rep.' : 'egypt',
               'gambia, the' : 'gambia', 'iran, islamic rep.' : 'iran', 'korea, rep.' : 's. korea',
               'kyrgyz republic' : 'kyrgyzstan', 'russian federation' : 'russia',
                   'slovak republic' : 'slovakia', 'venezuela, rb' : 'venezuela'}

# retaining only common indexes of covid and predictor dataframe
def retain_common_index(pred_df, covid_df, country_map):
    # replace the indexes in predictor dataframe with the covid dataframe index value
    pred_indexes = pred_df.index.tolist()
    for key, value in country_map.items():
        idx = pred_indexes.index(key)
        pred_indexes[idx] = value
        pred_df.index = pred_indexes

    index_to_retain = intersection(covid_df.index.tolist(), predictor_df.index.tolist())
    covid_df = covid_df.loc[index_to_retain]
    pred_df = pred_df.loc[index_to_retain]
    return covid_df, pred_df


def equalize(covid_df, predictor_df):

    # Drop entries from covid dataframe which have NA/missing values in the column deaths_per_1M
    covid_df.dropna(inplace=True, subset=['deaths_per_1M'])

    # the numerical value are stored as strings in the dataframe, with commas
    # Removing comma and converting to numeric value
    covid_df.replace(',', '', regex=True, inplace=True)
    covid_df[covid_df.columns] = covid_df[covid_df.columns].apply(pd.to_numeric, errors='coerce')

    spell_error_detect(sorted(uncommon(predictor_df.index.tolist(), covid_df.index.tolist())), sorted(uncommon(covid_df.index.tolist(), predictor_df.index.tolist())))

    return retain_common_index(predictor_df, covid_df, country_map)

covid_df = pd.read_csv(data_dir + 'covid_worldometer.csv', index_col=0)
predictor_df = pd.read_csv(csv_dir + "filtered_country.csv", index_col=0)

# Convert indexes of predictor and covid dataframes to contain only lower case
predictor_df.index = predictor_df.index.str.lower()
covid_df.index = covid_df.index.str.lower()

covid_df, predictor_df = equalize(covid_df, predictor_df)
print("\nGenerating: {}, {}".format(csv_dir+'predictor.csv', csv_dir+'covid.csv'))
predictor_df.to_csv(csv_dir + 'predictor.csv')
covid_df.to_csv(csv_dir + 'covid.csv')

