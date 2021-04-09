#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from pandasql import sqldf
sql=lambda q: sqldf(q,globals())
import re

#Pie Chart Visualization of Payment Area
df = pd.read_csv("yes.csv")
df_pay_area = sql("""
SELECT `Payment_Area`,COUNT(*) as Total
FROM df
group by `Payment_Area`
order by Total desc
limit 6
""")

df_pay_area.set_index("Payment_Area")
colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'pink']
explode_list = [0.1, 0,0.1, 0,0.1, 0] # ratio for each continent with which to offset each wedge.

plt.rcParams.update({'font.size': 13})

df_pay_area['Total'].plot(kind='pie',
                            figsize=(15, 6),
                            autopct='%1.1f%%',
                            startangle=90,
                            shadow=True,
                            labels=None,         # turn off labels on pie chart
                            pctdistance=1.12,    # the ratio between the center of each pie slice and the start of the text generated by autopct
                            colors=colors_list,  # add custom colors
                            explode=explode_list # 'explode' lowest 3 payment types
                            )

# scale the title up by 12% to match pctdistance
plt.title('Distribution by Payment Area', y=1.05)
plt.axis('equal')
# add legend
plt.legend(labels=df_pay_area.index, loc='upper left')
plt.savefig("pay_area.png")



#Bar graph for Top 6 Debits
df_from_debit = sql("""
SELECT `From`,SUM(`Debit`) as Total
FROM df
group by `From`
order by Total desc
limit 6
""")

df_from_debit.set_index("From",inplace=True)
df_from_debit.plot(kind='bar')

plt.rcParams.update({'font.size': 17})
plt.ylabel("Total Amount")
plt.xlabel("Entity")
plt.savefig("Debit.png",bbox_inches = 'tight')



#Bar graph for Top 6 Credits
df_from_credit = sql("""
SELECT `From`,SUM(`Credit`) as Total
FROM df
group by `From`
order by Total desc
limit 6
""")

df_from_credit.set_index("From",inplace=True)
df_from_credit.plot(kind='bar')

plt.rcParams.update({'font.size': 17})
plt.ylabel("Total Amount")
plt.xlabel("Entity")
plt.savefig("Credit.png",bbox_inches = 'tight')