from dotenv import load_dotenv
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel,Field
from langchain.agents import create_agent
import os
from langchain_groq import ChatGroq



class RequiredElements(BaseModel):
    squareMeters: float | None = Field(gt=0,default=None,description="Apartment area in square meters.")
    rooms: int | None = Field(gt=0,default=None,description="Number of rooms.")

    floor: int | None = Field(ge=0,default=None,description="Floor on which the apartment is located.")

    buildYear: int | None = Field(gt=1900,default=None,description="Year the building was built.")

    centreDistance: float | None = Field(default=None,description="Distance from Warsaw city centre in kilometres.(If distance doesn't cover the district guide the user and tell him possible solutions)")

    condition: str | None = Field(default=None,description="Apartment condition. One of: premium,low.(If user gave something different decide to which one is more similar and choose from premium or low)")

    hasParkingSpace: int | None = Field(default=None,description="Whether the apartment has a parking space, 1-has, 0-doesnt have.(Don't write the part 0-no 1-yes, you have to convert this to 0 or one)")

    hasBalcony: int | None = Field(default=None,description="Whether the apartment has a balcony,  1-has, 0-doesnt have.")

    hasElevator: int | None = Field(default=None,description="Whether the building has an elevator,  1-has, 0-doesnt have.")

    hasSecurity: int | None = Field(default=None,description="Whether the building has security,  1-has, 0-doesnt have.")

    hasStorageRoom: int | None = Field(default=None,description="Whether the apartment has a storage room,  1-has, 0-doesnt have.")

    district: str | None = Field(default=None,description="District of Warsaw where the apartment is located.")


class AssistantResponse(BaseModel):
    message:str =Field(description="Assistant response naturally to users answers.")

    completed:bool=Field(default=False,description= "True only when all required data is completed")

    estateData: RequiredElements = Field(description="Estate data collected so far")



class EstateAssistant:
    def __init__(self):
        load_dotenv()
        api_key=os.getenv("GROQ_API_KEY")
        self.llm=ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)
        self.agent=create_agent(model=self.llm,system_prompt=self._get_system_prompt(),response_format=ToolStrategy(AssistantResponse)  )
        self.chat_history=[]

    @staticmethod
    def _get_system_prompt():
        return """ You are a Warsaw estate assistant, that will help user to enter all needed data to make Machine Learning model prediction. Your task is to check if user entered all needed data and to check if all data is correct. Wrap this output in this format and provide no other text. You need to collect exactly these fields     squareMeters,rooms, floor, buildYear ,centreDistance, condition, hasParkingSpace, hasBalcony, hasElevator, hasSecurity, hasStorageRoom,district"""
    def sendMessage(self,user_input):
        messages = self.chat_history + [ {"role": "user","content": user_input}]

        result = self.agent.invoke({"messages": messages})
        response = result["structured_response"]
        self.chat_history.append({"role": "user","content": user_input})

        self.chat_history.append({"role": "assistant","content": response.message})

        return response

    def reset_conversation(self) :
        self.chat_history.clear()


if __name__ == "__main__":
    load_dotenv()
    GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

   # final_data=None

    agent=create_agent(model=llm,system_prompt="You are a Warsaw estate assistant, that will help user to enter all needed data to make Machine Learning model prediction. Your task is to check if user entered all needed data and to check if all data is correct. Wrap this output in this format and provide no other text. You need to collect exactly these fields     squareMeters,rooms, floor, buildYear ,centreDistance, condition, hasParkingSpace, hasBalcony, hasElevator, hasSecurity, hasStorageRoom,district", response_format=ToolStrategy(AssistantResponse))

    #chat history list
    chat_history=[]

    print("Assistant: Hi, I am your estate assistant, what can I do for you?(If you want to exit type stop)")

    while True:
        user_input=input("You:".strip())
        if user_input.lower() =='stop':
            print("Thank you, goodbye!")
            break
        messages=chat_history+[{"role":"user","content":user_input}]
        result=agent.invoke({"messages":messages})

        try:
            required_data = result["structured_response"]
            print(required_data.message)
            if required_data.completed:
                print("All data have been completed, thank you")
                break

        except Exception as e:
            reply=str(e)
            break

        #update chat history
        chat_history.append({"role":"user","content":user_input})
        chat_history.append({"role": "assistant", "content": str(required_data)})

    print("data retrieved from chat:")
    print(required_data.estateData)

