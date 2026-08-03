import pandas as pd
import geopandas as gpd


def input_data():
    meters=input("Enter the number of meters: ")
    rooms=input("Enter the number of rooms: ")
    floors=input("Enter the number of floor: ")
    years=input("Enter the build year: ")
    centres=input("Enter the centre distance: ")
    cond=input("Enter the condition(premium/low): ").lower()
    parking=input("does it have parking?(1-yes, 0-no): ")
    balcony=input("does it have balcony?(1-yes, 0-no): ")
    elevator=input("does it have elevator?(1-yes, 0-no): ")
    security=input("does it have security?(1-yes, 0-no): ")
    storage=input("does it have storage?(1-yes, 0-no): ")
    num=input("Choose number of district from the list:12: 'Targówek', 3: 'Wola', 15: 'Bielany', 9: 'Śródmieście', 2: 'Mokotów', 11: 'Ursus', 17: 'Bemowo', 0: 'Żoliborz', 16: 'Białołęka', 1: 'Praga-Południe', 8: 'Ursynów', 14: 'Ochota', 4: 'Wilanów', 10: 'Praga-Północ', 13: 'Rembertów', 6: 'Wawer', 7: 'Włochy', 5: 'Wesoła': ")
    mapping={"premium":1,"low":0}
    cond=mapping[cond]


    df=pd.DataFrame({
        "squareMeters":[meters],
        "rooms":[rooms],
        "floor":[floors],
        "buildYear":[years],
        "centreDistance":[centres],
        "condition":[cond],
        "hasParkingSpace":[parking],
        "hasBalcony":[balcony],
        "hasElevator":[elevator],
        "hasSecurity":[security],
        "hasStorageRoom":[storage],
        "district_number":[num],
    })
    return df


def district2num(df):
    distDict={'Targówek':12 , 'Wola':3 , 'Bielany': 15, 'Śródmieście':9 , 'Mokotów': 2, 'Ursus':11 , 'Bemowo': 17, 'Żoliborz':0 , 'Białołęka':16 , 'Praga-Południe': 1, 'Ursynów': 8, 'Ochota': 14, 'Wilanów': 4, 'Praga-Północ': 10, 'Rembertów': 13, 'Wawer': 6, 'Włochy': 7, 'Wesoła': 5}
    if df["district"] not in distDict.keys():
        print("Given district is not valid")
        return df
    else:
        df["district_number"]=distDict[df["district"]]
        del df["district"]
        mapping = {"premium": 1, "low": 0}
        df["condition"] = mapping[df["condition"]]
        return df



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

