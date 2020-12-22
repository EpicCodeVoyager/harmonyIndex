from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import preprocessing
import pandas as pd

csv_dir = './intermediate_results/'

def get_pca_df2(df):
    data_scaled = pd.DataFrame(preprocessing.scale(df), columns=df.columns)
    # PCA
    pca = PCA(n_components=36)
    pca.fit_transform(data_scaled)
    # Dump components relations with features:

    y = pd.DataFrame(pca.components_, columns=data_scaled.columns, index=[str(x) for x in range(36)])
    y.to_csv(csv_dir + "pca2.csv")

def get_pca_df(df):
    x = StandardScaler().fit_transform(df)  # Standardise the columns data and return a Numpy array
    print(type(x))
    pca = PCA(n_components=36)  # PCA object created
    #x = np.nan_to_num(x)
    pcaComp = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=pcaComp, columns=["pca_"+x for x in df.columns.to_list()])
    print("**************")
    principalDf.to_csv(csv_dir + 'pca-4d.csv')
    pca_list = pca.explained_variance_ratio_
    pca_sum_list = pca.explained_variance_ratio_.cumsum()
    for x in pca_list:
        print(x)
    for index, y in enumerate(pca_sum_list, start=1):
        print(index, y)
    return x

