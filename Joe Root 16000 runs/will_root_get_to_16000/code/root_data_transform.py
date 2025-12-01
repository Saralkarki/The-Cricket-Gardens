import pandas as pd
from pathlib import Path

root_dir = Path(__file__).parent.parent
Path.cwd()
df = pd.read_csv(root_dir /"data/Joe_root_career_stats.csv")

# overall record
df_overall = df[0:1]
# vs country specific
df_country = df[1:11]

# vs country and venue country
df_country_venue = df[11:21]


# year wise
df_years = df[29:43]

## Save all to data folder
df_overall.to_csv(root_dir / "data/joe_root_overall.csv", index=False)
df_country.to_csv(root_dir / "data/joe_root_country.csv", index=False)
df_country_venue.to_csv(root_dir / "data/joe_root_country_venue.csv", index=False)
df_years.to_csv(root_dir / "data/joe_root_years.csv", index=False)
