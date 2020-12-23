from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
from regressor import sm_fit

csv_dir = './intermediate_results/'
plots_dir = './plots/'


def plot_linear_fit(column):
    plt.figure(figsize=(10, 6))
    x_l = x[column].values.reshape(-1, 1)
    y_l = y.values.reshape(-1, 1)
    model2 = LinearRegression()
    model2.fit(x_l, y_l)
    plt.style.use('bmh')
    plt.xlabel(column)
    plt.ylabel('Deaths Per Million')
    plt.scatter(x_l, y_l, color='g', alpha=0.5)
    plt.plot(x_l, model2.predict(x_l), color='b', linewidth=0.5)
    plt.savefig(plots_dir + column + '.png')


def plot_deaths_per_million(y):
    plt.figure()
    y.sort_values(by=["deaths_per_1M"], inplace=True)
    x_l = y['country'].tolist()
    y_l = y['deaths_per_1M'].tolist()
    plt.style.use('bmh')
    fig, ax = plt.subplots(figsize=(20, 8))
    plt.axhline(y=0, color='red', linestyle=':', alpha=.55)
    plt.ylabel('Deaths Per Million')
    plt.xlabel('Country')
    plt.title('Covid Death Country Wise')
    plt.xticks(rotation=90)
    ax.plot(x_l, y_l, linestyle='solid', color="blue", linewidth=1, label="pnl")
    plt.savefig(plots_dir + 'Deaths_Per_Million_Chart' + '.png')


x = pd.read_csv(csv_dir + "reduced_predictors.csv", index_col=0)
y = pd.read_csv(csv_dir + "covid.csv", index_col=0)
y = y['deaths_per_1M']

fit = sm_fit(x, y)

# Obtain list of significant columns (p-value < 0.05)
to_plot = [j for (i, j) in zip(fit.pvalues.to_list(), fit.pvalues.axes[0].values.tolist()) if i <= 0.05]

# Plot fitting line for individual significant column vs deaths per million
for i in to_plot:
    plot_linear_fit(i)

# Plot number of deaths per million chart for each country ascending order
covid_deaths = pd.read_csv(csv_dir + "covid.csv")
plot_deaths_per_million(covid_deaths)
