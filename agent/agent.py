from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, format_instructions


class Required_elements(BaseModel):
    squareMeters: float
    rooms:int
    floor:int
    buildYear:int
    centreDistance:float
    condition:str
    hasParkingSpace:bool
    hasBalcony:bool
    hasElevator:bool
    hasSecurity:bool
    hasStorageRoom:bool
    district:str

if __name__ == "__main__":
    load_dotenv()
    llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash")
    parser=PydanticOutputParser(pydantic_object=Required_elements)
    response=llm.invoke("Hi, can you speak polish?")
    print(response)

    prompt=ChatPromptTemplate.from_messages([
        ("system",
            f"""You are an estate assistant, that will help user to enter all needed data to make Machine Learning model prediction. Your task is to check if user entered all needed data and to check if all data is correct. Wrap this output in this format and provide no other text\n {format_instructions}"""),
        ("placeholder",f"{chat_history}"),
        ("human",f"{query}"),
        ("placeholder",f"{agent_scratchpad}"),
    ]).partial(format_instructions=parser.get_format_instructions())
