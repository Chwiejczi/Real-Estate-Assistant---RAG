import pandas as pd
import geopandas as gpd

def prep_raw_data(path,path_shp):
    df = pd.read_csv(path)
    df = df[df["city"] == 'warszawa']
    df = df[df['type'].isin(['apartmentBuilding', 'blockOfFlats'])]
    df = df.drop(
        columns=['schoolDistance', 'clinicDistance', 'postOfficeDistance', 'kindergartenDistance', 'restaurantDistance',
                 'collegeDistance', 'pharmacyDistance', 'ownership', 'buildingMaterial', 'floorCount', 'city',
                 'poiCount', 'type', 'id'])
    df = df.dropna()
    mapping = {'yes': 1, 'no': 0}
    cols = ["hasParkingSpace", "hasBalcony", "hasSecurity", "hasStorageRoom","hasElevator"]
    for col in cols:
        df[col] = df[col].replace(mapping).astype(int)
    district = gpd.read_file(path_shp)
    df_dist = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"], crs="EPSG:4326"))
    df_dist = df_dist.to_crs(district.crs)
    combined = gpd.sjoin(df_dist, district, how="inner", predicate="within")
    combined.rename(columns={"nazwa_dzie": "district"}, inplace=True)
    combined.rename(columns={"index_right": "district_number"}, inplace=True)
    combined = combined.drop(columns=["latitude", "longitude", 'geometry'])
    mapping_cond = {'premium': 1, 'low': 0}
    combined['condition'] = combined['condition'].replace(mapping_cond).astype(int)

    return combined

if __name__ == '__main__':
    df=pd.read_csv("../raw/apartments_pl_2024_06.csv")
    #print(df)
    #we are going to take only estates from Warsaw
    df=df[df["city"]=='warszawa']

    #print(df["ownership"].unique())
    #we can drop ownership because all records as the same

    #print(df["hasParkingSpace"].unique())
    #we are going to exchange 'yes' and 'no' with 0 1

    #print(df["hasBalcony"].unique())
    #print(df["hasBalcony"].unique())
    #print(df["hasSecurity"].unique())
    #print(df["hasStorageRoom"].unique())
    #same as above


    #print(df["type"].unique())
    df=df[df['type'].isin(['apartmentBuilding','blockOfFlats']) ]
    #we are interested only in apartment buildings an block of flats
    #after that we can drop type column because it is str, so it could be problematic in nearest future

    df=df.drop(columns=['schoolDistance','clinicDistance','postOfficeDistance','kindergartenDistance','restaurantDistance','collegeDistance','pharmacyDistance','ownership','buildingMaterial','floorCount','city','poiCount','type','id'])



    #we are dropping missing rows it will be only about 1600 among 31000
    df=df.dropna()
    #print(df.isna().sum())
    #print(df.size)

    #we are going to exchange 'yes/no' values with 0/1
    mapping={'yes':1,'no':0}
    cols = ["hasParkingSpace","hasBalcony","hasSecurity","hasStorageRoom","hasElevator"]
    for col in cols:
        df[col]=df[col].replace(mapping).astype(int)
    #print(df['hasParkingSpace'])

    #now we are going to add column district based on latitude and longitude

    district=gpd.read_file("../raw/dzielnice_Warszawy/dzielnice_Warszawy.shp")

    df_dist=gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df["longitude"],df["latitude"],crs="EPSG:4326"))
    df_dist = df_dist.to_crs(district.crs)
    combined=gpd.sjoin(df_dist,district,how="inner",predicate="within")
    #print(combined.columns)
    combined.rename(columns={"nazwa_dzie":"district"},inplace=True)
    combined.rename(columns={"index_right": "district_number"}, inplace=True)

    #finally we can drop longitude and latitude and geometry
    combined=combined.drop(columns=["latitude","longitude",'geometry'])
    #print(combined[["district","district_number"]])
    #print(combined["geometry"])

    #we need to do something with condition, bcause it is represented by str
    #print(df["condition"].unique())
    mapping_cond={'premium':1, 'low':0}
    combined['condition']=combined['condition'].replace(mapping_cond).astype(int)
    #print(combined.info())

