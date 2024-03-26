# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

from pathlib import Path


datasets = Path('dataset/')

ph_gdf = gpd.read_file(datasets /'gadm41_PHL_shp/gadm41_PHL_1.shp')
ph_gdf.head(20)

educ_s = gpd.read_file(datasets / 'hotosm_phl_south_education_facilities_points_shp/hotosm_phl_south_education_facilities_points.shp')
educ_s.head()

educ_s.shape

educ_n = gpd.read_file(dataset_folder / 'hotosm_phl_north_education_facilities_points_shp/hotosm_phl_north_education_facilities_points.shp')
educ_n.head()

educ_n.shape

educ_sites = pd.concat([educ_n, educ_s])
educ_sites.head()

educ_sites.shape

educ_sites.crs


ax = ph_gdf.plot(figsize=(20, 14), color='white', edgecolor='dimgray')


ax = ph_gdf.plot(figsize=(20, 14), color='white', edgecolor='dimgray')
educ_sites.plot(ax=ax, column='amenity', legend=True, alpha=0.3)


educ_sites.plot(figsize=(20,14), column='amenity', legend=True, alpha=0.3)


# shapefile
educ_sites.to_file(dataset_folder / 'hotosm_phl_education_facilities.shp')

# geojson
educ_sites.to_file(dataset_folder / 'hotosm_phl_education_facilities.geojson', driver='GeoJSON')


ph_gdf.plot(figsize=(20, 14), color='white', edgecolor='dimgray')

ph_gdf.head(10)



educ_sites.head(10)


ph_educ_site_intersect = gpd.sjoin(ph_gdf, # left geodataframe (the polygons will be kept)
                               educ_sites, # right geodataframe (the ponit geometry will be dropped, but all attributes will be kept)
                               how='left', # default is 'inner' but we want to keep all the polygons! we don't want a map with a hole!
                               predicate='intersects' # default
                              )
ph_educ_site_intersect.head()

ph_educ_site_intersect.shape

educ_sites.shape


ph_educ_site_contains = gpd.sjoin(ph_gdf, # left geodataframe (the polygons will be kept)
                               educ_sites, # right geodataframe (the ponit geometry will be dropped, but all attributes will be kept)
                               how='left', # default is 'inner' but we want to keep all the polygons! we don't want a map with a hole!
                               predicate='contains' # points should be within the polygon
                              )
ph_educ_site_contains.head()

ph_educ_site_contains.shape



ph_educ_site_contains[ph_educ_site_contains.duplicated(subset='osm_id', keep=False)]


educ_sites.duplicated(subset='osm_id').sum()


educ_sites = educ_sites.drop_duplicates()
educ_sites.shape

ph_educ_site_contains = gpd.sjoin(ph_gdf, # left geodataframe (the polygons will be kept)
                               educ_sites, # right geodataframe (the ponit geometry will be dropped, but all attributes will be kept)
                               how='left', # default is 'inner' but we want to keep all the polygons! we don't want a map with a hole!
                               predicate='contains' # points should be within the polygon
                              )
ph_educ_site_contains.shape


ph_educ_site_contains.head(10)

ph_educ_site_contains.geometry.head()



ph_educ_site_contains.columns



ph_educ_site_contains.amenity.unique()

ph_educ_site_contains.building.unique()

ph_educ_site_contains.operatorty.unique()



ph_educ_site_contains[ph_educ_site_contains.amenity == 'bus_station']

clean_ph_educ_site = ph_educ_site_contains[ph_educ_site_contains.amenity != 'bus_station']
clean_ph_educ_site.shape

amenity_group = clean_ph_educ_site.groupby(['NAME_1','amenity'])['osm_id'].count().reset_index()
amenity_group.head()

operatorty_group = clean_ph_educ_site.groupby(['NAME_1','operatorty'])['osm_id'].count().reset_index()
operatorty_group.head()


amenity_pivot = pd.pivot_table(amenity_group, index='NAME_1', columns='amenity', values='osm_id', fill_value=0)
amenity_pivot.head()

operatorty_pivot = pd.pivot_table(operatorty_group, index='NAME_1', columns='operatorty', values='osm_id', fill_value=0)
operatorty_pivot.head()


# IMPORTANT: The GeoDataFrame should be on the OUTSIDE (left) of the merge so you keep the GeoDataFrame type
amenity_gdf = ph_gdf.merge(amenity_pivot, left_on='NAME_1', right_index=True, how='left')
amenity_gdf.fillna(0, inplace=True)
amenity_gdf.head()

# IMPORTANT: The GeoDataFrame should be on the OUTSIDE (left) of the merge so you keep the GeoDataFrame type
operatorty_gdf = ph_gdf.merge(operatorty_pivot, left_on='NAME_1', right_index=True, how='left')
operatorty_gdf.fillna(0, inplace=True)
operatorty_gdf.head()

print(ph_gdf.shape)
print(amenity_gdf.shape)
print(operatorty_gdf.shape)

amenity_gdf.columns

amenity_gdf = amenity_gdf[['GID_1', 'GID_0', 'COUNTRY', 'NAME_1', 'geometry', 'college',
       'kindergarten', 'school', 'university']]
amenity_gdf.columns = ['gid_1', 'gid_0', 'country', 'province', 'geometry', 'college',
       'kindergarten', 'school', 'university']

operatorty_gdf.columns

operatorty_gdf = operatorty_gdf[['GID_1', 'GID_0', 'COUNTRY', 'NAME_1', 'geometry',
       'consortium', 'corporation', 'government', 'private', 'public',
       'religious', 'university']]
operatorty_gdf.columns = ['gid_1', 'gid_0', 'country', 'province', 'geometry',
       'consortium', 'corporation', 'government', 'private', 'public',
       'religious', 'university']

amenity_gdf.plot(figsize=(20, 14), column='kindergarten', legend=True)
plt.title('Kindergarten');

operatorty_gdf.plot(figsize=(20, 14), column='religious', legend=True)
plt.title('Operatorty: Religious');

operatorty_gdf.plot(figsize=(20, 14), column='public', legend=True)
plt.title('Operatorty: Public');

operatorty_gdf.plot(figsize=(20, 14), column='private', legend=True)
plt.title('Operatorty: Private');

amenity_gdf.to_file(dataset_folder / 'ph_educ_by_amenity.geojson', driver='GeoJSON')

operatorty_gdf.to_file(dataset_folder / 'ph_educ_by_operatorty.geojson', driver='GeoJSON')