import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import datasets, linear_model
import statsmodels.api as sm
from scipy import stats

csv_dir = './intermediate_results/'
# Function to remove multi collinearity
def remove_highly_correlated_columns(x, threshold):
    corr_matrix = x.corr().abs()
    up_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

    to_drop = [column for column in up_tri.columns if any(up_tri[column] > threshold)]
    print('Dropping the following {} highly correlated columns: '.format(to_drop.__len__()))
    print(to_drop)

    for i in to_drop:
        x = x.drop(i, axis=1)
    return x


x = pd.read_csv(csv_dir + "predictor.csv", index_col=0)
y = pd.read_csv(csv_dir + "covid.csv", index_col=0)
y = y['deaths_per_1M']
x.columns = [col.replace('\'', '') for col in x.columns]
x.columns = [col.replace('(', '') for col in x.columns]
x.columns = [col.replace(')', '') for col in x.columns]

threshold = 0.7
x = remove_highly_correlated_columns(x, threshold)

model = LinearRegression()
model.fit(x, y)

r_sq = model.score(x, y)
print('\nCoefficient of determination:', r_sq)

X2 = sm.add_constant(x)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())

x.to_csv(csv_dir + 'reduced_predictors.csv')

