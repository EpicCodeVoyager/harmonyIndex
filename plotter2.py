from matplotlib import pyplot as plt
import pandas as pd
csv_dir = './intermediate_results/'

y = pd.read_csv(csv_dir + "covid.csv")
y.sort_values(by=["deaths_per_1M"], inplace = True)

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
plt.show()
