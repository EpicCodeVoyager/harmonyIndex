import pandas as pd
import ast
import numpy as np

csv_dir = './intermediate_results/'
threshold = 31

def imputator(thr):
    print("****Imputating the data...")
    df = pd.read_csv(csv_dir + 'raw_country.csv')
    df = df.set_index('Country')

    initial_num_of_rows = len(df.index)
    print('Initial number of rows: ' + str(initial_num_of_rows))
    df.replace(to_replace="..", value=np.NaN, inplace=True)
    df.dropna(inplace=True, thresh=thr) # keep rows containing at least 31 non null values
    df[df.columns] = df[df.columns].apply(pd.to_numeric, errors='coerce')
    df.fillna(df.mean(), inplace=True)

    print('Number of rows removed: ', initial_num_of_rows - len(df.index))
    print("Generating: {}".format(csv_dir + 'filtered_country.csv\n'))
    df.to_csv(csv_dir + 'filtered_country.csv')
    return df

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

for i in conjugate_list:
    res = i.split('^')
    df = pd.read_html(res[0])
    # Create Pandas series object with index as countries.
    s = pd.Series(df[0].loc[:, ast.literal_eval(res[1])].tolist(), index=df[0].iloc[:, 0].tolist())
    # Series created using pandas series object  as list. Else was giving Nan values
    frame[res[1]] = s # add series for each table-coulumn into initiated dataframe

# raw country data collected from internet
print("Generating: {}".format(csv_dir+'raw_country.csv'))
frame.to_csv(csv_dir + 'raw_country.csv')
corrected_frame = imputator(threshold)
