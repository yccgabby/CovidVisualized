import pandas as ps
import matplotlib.pyplot as ppt
import matplotlib.ticker as tk
from matplotlib.dates import DateFormatter

# Reading data from URL into a Pandas dataframe and only selecting specific countries
df = ps.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])
cn = ['Canada', 'Germany', 'United Kingdom', 'US', 'France', 'China', 'Italy', 'Spain', 'Iran', 'Switzerland', 'Turkey']
df = df[df['Country'].isin(cn)]

# Add summary column that aggregates the number of confirmed cases, recovered cases and deaths
df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)

# Replace old "confirmed, recovered, deaths" columns with new country columns, reset
# Replace indexes with dates, and populate data values with total number of cases
df = df.pivot(index='Date', columns='Country', values='Cases')
cn = list(df.columns)
cv = df.reset_index('Date')
cv.set_index(['Date'], inplace=True)
cv.columns = cn

# Find # of cases per 100000 by dividing total number of cases in one country by population, then multiply by 100000
pop = {'Canada': 37664517, 'Germany': 83721496, 'United Kingdom': 67802690, 'US': 330548815, 'France': 65239883,
       'China': 1438027228, 'Italy': 60550075, 'Spain': 47007367, 'Iran': 83753963, 'Switzerland': 8640750,
       'Turkey': 84138381}
cap = cv.copy()
for c in list(cap.columns):
    cap[c] = cap[c] / pop[c] * 100000

# Choosing colors and style
colors = {'Canada': '#FF5733', 'China': '#FFB533', 'France': '#FFEC33', 'Germany': '#BEFF33', 'Iran': '#33FF3C',
          'Italy': '#33FFA8', 'Spain': '#33FFFF', 'Switzerland': '#3393FF', 'Turkey': '#4F33FF', 'US': '#BE33FF',
          'United Kingdom': '#FF33A8'}
ppt.style.use('fivethirtyeight')

# Creating the visualization
p = cv.plot(figsize=(25, 18), color=list(colors.values()), linewidth=5, legend=True)
p.yaxis.set_major_formatter(tk.StrMethodFormatter('{x:,.0f}'))
p.grid(color='#d4d4d4')
p.set_xlabel('Date')
p.set_ylabel('# of Cases')

for c in list(colors.keys()):
    p.text(x=cv.index[-1], y=cv[c].max(), color=colors[c], s=c, weight='bold')

p.text(x=cv.index[10], y=int(cv.max().max()) + 45000, s="COVID-19 Cases by Country", fontsize=23, weight='bold',
       alpha=.75)
p.text(x=cv.index[10], y=int(cv.max().max()) + 15000, s="For Canada, Germany, the United Kingdom, the United States, "
                                                       "France, China, Italy, Spain, Iran, Switzerland and "
                                                       "Turkey\nIncludes Current Cases, Recoveries, and Deaths",
       fontsize=16, alpha=.75)
p.text(x=cap.index[1], y=-100000, s='datagy.io                      Source: '
                                    'https://github.com/datasets/covid-19/blob/master/data/countries'
                                    '-aggregated.csv', fontsize=10)

ppt.show(block=True)
