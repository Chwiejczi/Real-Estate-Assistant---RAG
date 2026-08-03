import pandas as pd
from agent.agent import EstateAssistant
from rag.rag import RAG_agent
from data.processed.data_cleaning import prep_raw_data
import joblib

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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ##df=prep_raw_data(path='data/raw/apartments_pl_2024_06.csv',path_shp='data/raw/dzielnice_Warszawy/dzielnice_Warszawy.shp')
    ##print(df[df["district"]=="Wola"])
    ##print(df.info())
    ##temp=df[['district','district_number']].drop_duplicates()
    ##names_numbers_distr=dict(zip(temp['district_number'],temp['district']))
    ##print(names_numbers_distr)
    ###{12: 'Targówek', 3: 'Wola', 15: 'Bielany', 9: 'Śródmieście', 2: 'Mokotów', 11: 'Ursus', 17: 'Bemowo', 0: 'Żoliborz', 16: 'Białołęka', 1: 'Praga-Południe', 8: 'Ursynów', 14: 'Ochota', 4: 'Wilanów', 10: 'Praga-Północ', 13: 'Rembertów', 6: 'Wawer', 7: 'Włochy', 5: 'Wesoła'}
    ##print(df.shape)
##
    ##model=joblib.load('model/final_model.pkl')
    ##df=input_data()
    ##pred=model.predict(df)
    ##print(f"predicted price:{pred}")
    rag=RAG_agent()
    res=rag.sendMessage("ile dzieci chodzi do warszawskich szkół?")
    print(res)



    agent =EstateAssistant()


    print("Assistant: Hi, I am your estate assistant, what can I do for you?(If you want to exit type stop)")
    response=None
    while True:
        user_input = input("You:".strip())
        if user_input.lower() == 'stop':
            print("Thank you, goodbye!")
            break

        try:
            response=agent.sendMessage(user_input)
            print(response.message)
            if response.completed:
                print("All data have been completed, thank you")
                break

        except Exception as e:
            reply = str(e)
            break
    if response is None:
        exit()

    #print("data retrieved from chat:")
    data=response.estateData
    data=data.model_dump()
    agent.reset_conversation()
    #print(type(data))
    data=district2num(data)

    model=joblib.load('model/final_model.pkl')
    df=pd.DataFrame([data])
    pred=model.predict(df)
    print(f"predicted price:{pred}")
