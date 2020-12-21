import pandas as pd
import ast
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np


def imputator():
    print("****Imputating the data...")
    df = pd.read_csv('./' + 'my_df.csv')
    df = df.set_index('Country')
    print(df.head())

    countries = df.index.tolist()
    naList = []  # list of countries that has missing values

    # Creating a list of the countries that has missing values
    for i in range(len(df.index)):
        if df.iloc[i].isnull().sum() != 0:
            print(countries[i], " : ", df.iloc[i].isnull().sum())
            naList.append(i)

    initial_num_of_rows = len(df.index)

    # Most of the countries that have NA values have missing values for most of the columns.
    # 34 and 30 out of 36 columns

    # removing those countries from the data frame
    for i in naList:
        df = df.drop(index=countries[i])

    df_removedNA = df
    print('\nNumber of columns removed: ', initial_num_of_rows - len(df_removedNA.index))
    df_removedNA.to_csv('./' + 'my_df_removedNA.csv')
    return df_removedNA


def get_pca_df(country_df):
    x = StandardScaler().fit_transform(country_df)
    #print(x.shape)
    pca = PCA(n_components=4)
    # ToDo: Need a better cleanup.
    #x = np.nan_to_num(x)
    pcaComp = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=pcaComp
                                , columns=['pc1', 'pc2', 'pc3', 'pc4'])
    print("**************")
    principalDf.to_csv('./'+ 'pca-4d.csv')
    pca_list = pca.explained_variance_ratio_
    for x in pca_list:
        print(x)
    return x


# Reading tables' and columns' names
file = open('tables_columnsName.txt', 'r')
Lines = file.readlines()
conjugate_list = [x.strip('\n') for x in Lines if x != '\n']


print(conjugate_list)
print(conjugate_list.__len__())

# Initiating dataframe that from the table that has the highest number of rows
# Setting the first row of Counrty names as index

df0 = pd.read_html('data/economic_unemployment.xls')
index0 = df0[0].loc[:, ('Unnamed: 0_level_0', 'Unnamed: 0_level_1')]
data = df0[0].loc[:, ('Unemployment, male (% of male labor force) (modeled ILO estimate)', '2018')].tolist()

# Print number of rows of the initiated dataframe
print(len(index0))

frame = pd.DataFrame({'Country':index0, "('Unemployment, male (% of male labor force) (modeled ILO estimate)', '2018')":data})
frame = frame.set_index('Country')
print(frame)

for i in conjugate_list:
    res = i.split('^')
    df = pd.read_html(res[0])
    # Create Pandas series object with index as countries.
    s = pd.Series(df[0].loc[:, ast.literal_eval(res[1])].tolist(), index=df[0].iloc[:, 0].tolist())
    # Series created using pandas series object  as list. Else was giving Nan values
    # print(s)
    # print(len(s)) # Checking longest column to use its index as index for all. economic_unemployment -> 264 rows. Modified code above to vreate main dataframe with index as countries
    frame[res[1]] = s # add series for each table into main dataframe

print(frame)
# ToDo: Pay attention here.
frame.replace(to_replace="..", value=0, inplace=True)
frame.to_csv('./'+'my_df.csv')
corrected_frame = imputator()
get_pca_df(corrected_frame)
