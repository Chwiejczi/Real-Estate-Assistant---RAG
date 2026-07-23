from data.processed.data_cleaning import prep_raw_data
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df=prep_raw_data(path='data/raw/apartments_rent_pl_2024_06.csv',path_shp='data/raw/dzielnice_Warszawy/dzielnice_Warszawy.shp')
    print(df[df["district"]=="Wola"])
    print(df.info())
    temp=df[['district','district_number']].drop_duplicates()
    names_numbers_distr=dict(zip(temp['district_number'],temp['district']))
    print(names_numbers_distr)
    #{12: 'Targówek', 3: 'Wola', 15: 'Bielany', 9: 'Śródmieście', 2: 'Mokotów', 11: 'Ursus', 17: 'Bemowo', 0: 'Żoliborz', 16: 'Białołęka', 1: 'Praga-Południe', 8: 'Ursynów', 14: 'Ochota', 4: 'Wilanów', 10: 'Praga-Północ', 13: 'Rembertów', 6: 'Wawer', 7: 'Włochy', 5: 'Wesoła'}
