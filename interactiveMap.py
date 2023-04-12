from io import StringIO
import pandas as pd
import numpy as np
import math
import altair as alt
import os
import geopandas as gp
import matplotlib as mpl
import descartes as dc
import folium
from IPython.display import display

df = pd.read_csv(
    "/Users/ajcaesar/Desktop/interactiveAOImap/AOI Updated Comparisons  - imported from collect earth online-3 copy.csv")
dfcheck = pd.DataFrame(
    columns=['AOI', 'NumCompleted', 'Complete', 'lat', 'lon', 'Avg Time'])
df2 = pd.DataFrame(columns=['AOI', 'lat', 'lon', 'avg time'])
dfTime = pd.DataFrame(columns=['AOI', 'Avg Time'])

i = 0
r = 0
numSet = 0
while i < 111:
    x = 0
    numCompleted = 0
    totalTime = 0
    Finished = True
    while x < 37:
        y = df.iloc[37 * i + x, 7]
        time = df.iloc[37 * i + x, 12]
        if not pd.isna(y):
            numCompleted += 1
            if time < 1000:
                totalTime += time
        else:
            Finished = False
        x += 1
    dfcheck.at[i, 'AOI'] = i
    dfcheck.at[i, 'NumCompleted'] = numCompleted
    dfcheck.at[i, 'Complete'] = Finished
    dfcheck.at[i, 'lat'] = df.iloc[i*37, 3]
    dfcheck.at[i, 'lon'] = df.iloc[i*37, 2]
    if Finished:
        dfcheck.at[i, 'Avg Time'] = totalTime / 37
        numSet += 1
        df2.at[r, 'AOI'] = i
        dfTime.at[r, 'AOI'] = i
        df2.at[r, 'lat'] = dfcheck.iloc[i, 3]
        df2.at[r, 'lon'] = dfcheck.iloc[i, 4]
        dfTime.at[r, 'Avg Time'] = totalTime / 37
        r += 1
    i += 1


ww = alt.Chart(dfTime, title='Average Time (seconds) per plot for 68 Completed AOIs').mark_bar(
).encode(x="AOI", y="Avg Time")

z = True
for AOI in df["AOI"]:
    if dfTime["AOI"].isin([AOI]).any():
        z = False
    else:
        row = df[df["AOI"] == AOI]
        index = row.index[0]
        df = df.drop(index)
zz = 0
while zz < len(df):
    qq = df.iloc[zz]['analysis_duration']
    if qq > 1500:
        df.iloc[zz, df.columns.get_loc('analysis_duration')] = np.nan
    zz += 1

df.reset_index(drop=True, inplace=True)


dfLandcoverDistributions = pd.DataFrame(columns=['AOI', 'sumIrrigationDitch', 'sumGrass', 'sumRivers/Streams', 'sumImperviousSurface', 'sumLake/Pond',
                                                 'sumCultivatedVegetation', 'sumBareGround', 'sumBuilding', 'sumTreatedPool', 'sumTrees/Canopy', 'sumUnknown', 'sumBush/Shrub',
                                                 'sumShadow'])
repeats = 0
while repeats < 68:
    sumIrrigationDitch = 0
    sumGrass = 0
    sumRiversXStreams = 0
    sumImperviousSurface = 0
    sumLakeXPondXContainer = 0
    sumCultivatedVegetation = 0
    sumBareGround = 0
    sumBuilding = 0
    sumTreatedPool = 0
    sumTreesXCanopyCover = 0
    sumUnknown = 0
    sumBushXShrub = 0
    sumShadow = 0
    AOInum = 0
    while AOInum < 37:
        sumIrrigationDitch += df.iloc[37*repeats + AOInum, 15]
        sumGrass += df.iloc[37*repeats + AOInum, 16]
        sumRiversXStreams += df.iloc[37*repeats + AOInum, 17]
        sumImperviousSurface += df.iloc[37*repeats + AOInum, 18]
        sumLakeXPondXContainer += df.iloc[37*repeats + AOInum, 19]
        sumCultivatedVegetation += df.iloc[37*repeats + AOInum, 20]
        sumBareGround += df.iloc[37*repeats + AOInum, 21]
        sumBuilding += df.iloc[37*repeats + AOInum, 22]
        sumTreatedPool += df.iloc[37*repeats + AOInum, 23]
        sumTreesXCanopyCover += df.iloc[37*repeats + AOInum, 24]
        sumUnknown += df.iloc[37*repeats + AOInum, 25]
        sumBushXShrub += df.iloc[37*repeats + AOInum, 26]
        sumShadow += df.iloc[37*repeats + AOInum, 27]
        AOInum += 1
    dfLandcoverDistributions.at[repeats, 'AOI'] = df.iloc[37*repeats, 0]
    dfLandcoverDistributions.at[repeats,
                                'sumIrrigationDitch'] = sumIrrigationDitch
    dfLandcoverDistributions.at[repeats, 'sumGrass'] = sumGrass
    dfLandcoverDistributions.at[repeats,
                                'sumRivers/Streams'] = sumRiversXStreams
    dfLandcoverDistributions.at[repeats,
                                'sumImperviousSurface'] = sumImperviousSurface
    dfLandcoverDistributions.at[repeats,
                                'sumLake/Pond'] = sumLakeXPondXContainer
    dfLandcoverDistributions.at[repeats,
                                'sumCultivatedVegetation'] = sumCultivatedVegetation
    dfLandcoverDistributions.at[repeats, 'sumBareGround'] = sumBareGround
    dfLandcoverDistributions.at[repeats, 'sumBuilding'] = sumBuilding
    dfLandcoverDistributions.at[repeats, 'sumTreatedPool'] = sumTreatedPool
    dfLandcoverDistributions.at[repeats,
                                'sumTrees/Canopy'] = sumTreesXCanopyCover
    dfLandcoverDistributions.at[repeats, 'sumUnknown'] = sumUnknown
    dfLandcoverDistributions.at[repeats, 'sumBush/Shrub'] = sumBushXShrub
    dfLandcoverDistributions.at[repeats, 'sumShadow'] = sumShadow
    repeats += 1


def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


csv = convert_df(dfLandcoverDistributions)

dfDistributions = pd.read_csv(
    '/Users/ajcaesar/Desktop/interactiveAOImap/AOI junk - Distribution of Landcover by type.csv')
print(dfDistributions)
print(dfDistributions.iloc[0, 1])

for column in dfDistributions:
    print(column)

data_top = dfDistributions.head()

# iterating the columns
for row in data_top.index:
    print(row, end=" ")

# x = alt.Chart(dfDistributions).transform_fold(
    #  ['sumTrees/Canopy', 'sumImperviousSurface', 'sumGrass', 'sumRivers/Streams','sumLake/Pond','sumCultivatedVegetation',
    #   'sumBareGround','sumBuilding,sumTreatedPool','sumUnknown','sumBush/Shrub','sumShadow,sumIrrigationDitch'], as_=['column', 'value']
# ).mark_bar().encode(
 #   x='column:N',
    #  y='value:Q',
    #  color=alt.Color('label:N', scale=None))

row = pd.DataFrame(dfDistributions, index=[0])

# Melt the row into a dataframe with two columns
melted = row.melt(var_name='category', value_name='value')

#  color=alt.Color(['#964B00', '#808080', '#FFFF00', '#FFA500', '#AAFF00','#FF0000', '#ADD8E6', '#00008B', '#87CEEB', '#000000', '#0096F', '#023020', '#808080']).scale(None)
# Create a bar chart using Altair
bar_chart = alt.Chart(melted).mark_bar().encode(
    x='category',
    y='value'
)


# Display the chart in VS Code using IPython's display function

html = bar_chart.to_html()
with open('xxx.html', 'w') as f:
    f.write(html)

map = folium.Map(location=[40, -75], zoom_start=1)

# Add markers to the map
x = 0
while x < 68:
    row = pd.DataFrame(dfDistributions, index=[x])
# Melt the row into a dataframe with two columns
    melted = row.melt(var_name='category', value_name='value')
#  color=alt.Color(['#964B00', '#808080', '#FFFF00', '#FFA500', '#AAFF00','#FF0000', '#ADD8E6', '#00008B', '#87CEEB', '#000000', '#0096F', '#023020', '#808080']).scale(None)
# Create a bar chart using Altair
    bar_chart = alt.Chart(melted).mark_bar().encode(
        y=alt.X('category', title='Landcover Category'),
        x=alt.Y('value', title='Num_Plots (out of 3700)')
    )
    vis1 = bar_chart.to_json()
    folium.Marker([df2.iloc[x, 1], df2.iloc[x, 2]], popup=folium.Popup(max_width=450).add_child(
        folium.VegaLite(vis1, width=300, height=400)), tooltip='See Landcover Distribution').add_to(map)
    print(x)
    x += 1

map.save("Final_CompletedAOI_Map.html")
