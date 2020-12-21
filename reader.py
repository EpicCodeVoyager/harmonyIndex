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

    initial_num_of_rows = len(df.index)
    print(initial_num_of_rows)
    df.replace(to_replace="..", value=np.NaN, inplace=True)
    df.dropna(inplace=True, thresh=31) # keep rows containing at least 31 non null values
    df[df.columns] = df[df.columns].apply(pd.to_numeric, errors='coerce')
    df.fillna(df.mean(), inplace=True)

    print('\nNumber of columns removed: ', initial_num_of_rows - len(df.index))

    df.to_csv('./' + 'my_df_removedNA.csv')
    return df


def get_pca_df(df):
    x = StandardScaler().fit_transform(df) # Standardise the columns data and return a Numpy array
    print(type(x))
    exit(1)
    pca = PCA(n_components=36) # PCA object created
    #x = np.nan_to_num(x)
    pcaComp = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=pcaComp, columns=["pca_"+x for x in df.columns.to_list()])
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


#print(conjugate_list) # List of tables and columns
#print(conjugate_list.__len__()) # 36 total columns

# Initiating dataframe that from the table that has the highest number of rows
# Setting the first row of Counrty names as index

df0 = pd.read_html('data/economic_unemployment.xls')
index0 = df0[0].loc[:, ('Unnamed: 0_level_0', 'Unnamed: 0_level_1')]
data = df0[0].loc[:, ('Unemployment, male (% of male labor force) (modeled ILO estimate)', '2018')].tolist()

# Print number of rows of the initiated dataframe
#print(len(index0))

frame = pd.DataFrame({'Country':index0, "('Unemployment, male (% of male labor force) (modeled ILO estimate)', '2018')":data})
frame = frame.set_index('Country')
#print(frame)

for i in conjugate_list:
    res = i.split('^')
    df = pd.read_html(res[0])
    # Create Pandas series object with index as countries.
    s = pd.Series(df[0].loc[:, ast.literal_eval(res[1])].tolist(), index=df[0].iloc[:, 0].tolist())
    # Series created using pandas series object  as list. Else was giving Nan values
    frame[res[1]] = s # add series for each table-coulumn into initiated dataframe

#print(frame) # Collected dataframe

frame.to_csv('./'+'my_df.csv')
corrected_frame = imputator()
get_pca_df(corrected_frame)
