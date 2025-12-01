import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

root_dir = Path(__file__).parent.parent
Path.cwd()

df_overall = pd.read_csv(root_dir / "data/joe_root_overall.csv")
df_country = pd.read_csv(root_dir / "data/joe_root_country.csv")
df_country_venue = pd.read_csv(root_dir / "data/joe_root_country_venue.csv")
df_years = pd.read_csv(root_dir / "data/joe_root_years.csv")

# THe last row is the total sum, 
df_years = df_years.iloc[:-1]
df_years
# 
df_years['Span']
# convert span column in df_years to datetime year
df_years["Span"] = pd.to_datetime(df_years["Span"], format="%Y").dt.year

# create a new columns - number of times out
df_years['Outs'] = df_years['Inns'] - df_years['NO'] 


## graph the runs by years 
plt.figure(figsize=(10, 6))
plt.bar(df_years["Span"], df_years["Runs"])
plt.title("Joe Root Runs by Year")
plt.xlabel("Year")
plt.ylabel("Runs")
plt.xticks(rotation=45)
plt.tight_layout()
# plot anytime average is over 40 for any span change color
colors = ['green' if avg > 40 else 'red' for avg in df_years['Avg']]
plt.bar(df_years["Span"], df_years["Runs"], color=colors)
plt.show()

# Group runs and averages by year the column already has sum of years and avedrage
# df_years.groupby("Span").agg({"Mat":'sum',"Runs": "sum", "Avg": "mean"})
print(df_years[['Mat','Runs','Avg']])


# Group runs before and after 2021
df_years['Period'] = df_years['Span'].apply(lambda x: 'Before 2021' if x <= 2020 else 'Since 2021')
# cannot take average lke this this, the average column is already average
# so has to use the runs column to take average by Matches
# matches

df_years.columns

# Calculate correct average for each period: total runs / total matches
for period, group in df_years.groupby("Period"):
	total_runs = group["Runs"].sum()
	total_outs = group["Outs"].sum()
	total_matches = group['Mat'].sum()
	overall_avg = total_runs / total_outs if total_outs else float('nan')
	print(f"{period}: Runs = {total_runs}, Outs = {total_outs}, Overall Avg = {overall_avg:.2f}, Matches = {total_matches}")

# number of 100's before and after 2020
df_years['100s'] = df_years['100s'].fillna(0)
df_years.groupby("Period").agg({"100s": "sum"})

# Root average before and after 2020, but do not look at 2012 because he played
#only one match. Do not change it to zero. Just do not look at it, 


df_years_no_2012 = df_years[df_years['Span'] != 2012]
df_years
for period, group in df_years_no_2012.groupby("Period"):
	total_runs = group["Runs"].sum()
	total_outs = group["Outs"].sum()
	overall_avg = total_runs / total_outs if total_outs else float('nan')
	print(f"{period}: Runs = {total_runs}, Outs = {total_outs}, Overall Avg = {overall_avg:.2f}")
	
# plot now before 2021 and since 2021 averages and runs
# Plot averages and runs before 2021 and since 2021
period_stats = df_years.groupby('Period').agg({'Runs': 'sum', 'Outs': 'sum'})
period_stats['Avg'] = period_stats['Runs'] / period_stats['Outs']

fig, ax = plt.subplots(figsize=(8, 8))
bars = ax.bar(period_stats.index, period_stats['Avg'], color='orange', width=0.4, label='Average')
ax.set_ylabel('Average')
ax.set_xlabel('Period')
ax.set_title('Joe Root: Average and Runs Before 2021 vs Since 2021')

# Add total runs as text above each bar
for i, (idx, row) in enumerate(period_stats.iterrows()):
	ax.text(i, row['Avg'] + max(period_stats['Avg']) * 0.02, f"Runs: {int(row['Runs'])}",
			ha='center', va='bottom', fontsize=12, color='blue', fontweight='bold')

ax.legend(loc='upper left')
plt.tight_layout()
plt.show()