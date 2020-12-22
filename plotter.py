from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
from regressor import remove_highly_correlated_columns
import statsmodels.api as sm
csv_dir = './intermediate_results/'
reduced_predictors = pd.read_csv(csv_dir + 'reduced_predictors.csv', index_col=0)

x = pd.read_csv(csv_dir + "reduced_predictors.csv", index_col=0)
y = pd.read_csv(csv_dir + "covid.csv", index_col=0)
y = y['deaths_per_1M']
threshold = 0.7
print(x.columns)
x_l = x['Unemployment, male % of male labor force modeled ILO estimate, 2018'].values.reshape(-1, 1)

y_l = y.values.reshape(-1, 1)

print(x_l)
print('***')
print(x['Unemployment, male % of male labor force modeled ILO estimate, 2018'])
# X = data.iloc[:, 0].values.reshape(-1, 1) # values converts it into a numpy array
# Y = data.iloc[:, 1].values.reshape(-1, 1) # -1 means that calculate the dimension of rows, but have 1 column
# linear_regressor = LinearRegression() # create object for the class
# linear_regressor.fit(X, Y) # perform linear regression
# Y_pred = linear_regressor.predict(X)
# plt.scatter(X, Y)
# plt.plot(X, Y_pred, color='red')
# plt.show()

model2 = LinearRegression()
model2.fit(x_l, y_l)
plt.scatter(x_l, y_l, color='g')
# what does the model2.predict gives ??
plt.plot(x_l, model2.predict(x_l), color='k')
plt.show()
