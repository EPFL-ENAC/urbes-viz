Files

- Flows (.csv)
There are 3 flow files named as flows_{environment code}_{day of a year}_{hour of a day}_min{threshold person to filter minor flow}persons.csv
Each file has the grid ID of destination and origin grid and the counts of people

flows_1_199_10_min1persons.csv: OD matrix for 'work' 
flows_5_199_18_min1persons.csv: OD matrix for 'Indoor leisure'
flows_6_199_18_min1persons.csv: OD matrix for 'Outdoor'

- Grid (.shp)
The grid ID are defined in 500_grid_Vaud_Geneva_within.shp


- 24-hour temporal population in different environments in each grid (.gpkg)
file name: population_{environment code}_{day of a year}.gpkg 

environment code:
0: Home
1: Work
5: Indoor leisure
6: Outdoor
9: Hospitality
