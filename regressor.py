import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

csv_dir = './intermediate_results/'

# Function to remove highly multi collinear columns
def remove_highly_correlated_columns(x, threshold):
    corr_matrix = x.corr().abs()
    up_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

    to_drop = [column for column in up_tri.columns if any(up_tri[column] > threshold)]
    print('Dropping the following {} highly correlated columns: '.format(to_drop.__len__()))
    print(to_drop)

    for i in to_drop:
        x = x.drop(i, axis=1)
    return x

# Function to print summary of the model and return fit object
def sm_fit(x, y):

    # Using statsmodels for printing the regression summary
    x2 = sm.add_constant(x)
    model_sm = sm.OLS(y, x2)
    fit = model_sm.fit()
    print(fit.summary())
    return fit

# Function to print R square value of the model
def fit_score(x,y):
    model = LinearRegression()
    model.fit(x, y)
    r_square = model.score(x, y)
    print('\nCoefficient of determination:', r_square)


x = pd.read_csv(csv_dir + "predictor.csv", index_col=0)
y = pd.read_csv(csv_dir + "covid.csv", index_col=0)
y = y['deaths_per_1M']
x.columns = [col.replace('\'', '') for col in x.columns]
x.columns = [col.replace('(', '') for col in x.columns]
x.columns = [col.replace(')', '') for col in x.columns]

threshold = 0.7
x = remove_highly_correlated_columns(x, threshold)

fit_score(x, y)
sm_fit(x, y)

x.to_csv(csv_dir + 'reduced_predictors.csv')

