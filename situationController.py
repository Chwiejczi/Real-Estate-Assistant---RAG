from rag.rag import RAG_agent
from agent.agent import EstateAssistant
from data.processed.data_cleaning import district2num
import joblib
import pandas as pd

class controller():
    def __init__(self):
        self.rag=RAG_agent()
        self.assistant=EstateAssistant()
        self.model=joblib.load('model/final_model.pkl')
    def agent_selector(self, user_input):
        keywords=['price','cost','costs', 'value',"how much","worth","predict", "predict price","market value"]
        if any(keyword in user_input for keyword in keywords):
            print("Give me some details(If you want to exit type stop)")
            response = None
            while True:
                user_input = input("You:".strip())
                if user_input.lower() == 'stop':
                    print("Thank you, goodbye!")
                    break

                try:
                    response = self.assistant.sendMessage(user_input)
                    print(response.message)
                    if response.completed:
                        print("All data have been completed, thank you")
                        break

                except Exception as e:
                    reply = str(e)
                    break
            if response is None:
                exit()

            data = response.estateData
            data = data.model_dump()
            self.assistant.reset_conversation()
            data = district2num(data)
            df = pd.DataFrame([data])
            pred = self.model.predict(df)
            print(f"Predicted price:{pred}")

        else:
            res = self.rag.sendMessage(user_input)
            print(res)
