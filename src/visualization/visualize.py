import matplotlib.pyplot as pyplot
import seaborn as sns


# define data
data = [value1, value2, value3, ...]
labels = ['label1', 'label2', 'label3', ...]

# define Seaborn color palette to use
colors = sns.color_palette('pastel')[0:5]

# create pie chart
plt.pie(data, labels=labels, colors=colors, autopct='%.0f%%')
plt.show()
