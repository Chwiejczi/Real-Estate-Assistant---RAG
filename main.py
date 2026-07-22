from data.processed.data_cleaning import prep_raw_data
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df=prep_raw_data(path='data/raw/apartments_rent_pl_2024_06.csv',path_shp='data/raw/dzielnice_Warszawy/dzielnice_Warszawy.shp')
    print(df[df["district"]=="Wola"])

