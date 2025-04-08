#to clean the CSV data from WWF or whatever its called I forgot lol
import pandas as pd
import plotly.graph_objs as go
import json
import plotly
import numpy as np

#load and clean data
df = pd.read_csv("LPD_2024_public.csv")
year_cols = [str(y) for y in range(1950, 2021)]
data = df[year_cols].replace("NULL", pd.NA).astype("float")

#Chart 1: Average biodiversity index per year
avg_per_year = data.mean(axis=0, skipna=True)
line1 = go.Scatter(x=list(map(int, avg_per_year.index)), y=avg_per_year.values, mode='lines+markers')
fig1 = go.Figure(data=[line1])
fig1.update_layout(title="Average Biodiversity Index Over Time")
with open("app/static/avg_trend.json", "w") as f:
    f.write(json.dumps(json.loads(json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder))))

#Chart 2: Taxon class data
class_trends = []

#get top 4-6 most common classes with enough data
valid_classes = df["Class"].dropna().value_counts().head(6).index.tolist()

for class_name in valid_classes:
    class_group = df[df["Class"] == class_name]
    values = class_group[year_cols].replace("NULL", pd.NA).astype("float")

    #mean across species, then mean per year
    avg_by_year = values.mean(skipna=True)

    class_trends.append(go.Scatter(
        x=list(map(int, avg_by_year.index)),
        y=avg_by_year.values,
        mode="lines+markers",
        name=class_name
    ))

fig_class = go.Figure(data=class_trends)
fig_class.update_layout(
    title="Average Population Trend by Animal Class (1950-2020)",
    xaxis_title="Year",
    yaxis_title="Average Population Estimate",
    legend_title="Class"
)

with open("app/static/species_trends.json", "w") as f:
    f.write(json.dumps(json.loads(json.dumps(fig_class, cls=plotly.utils.PlotlyJSONEncoder))))