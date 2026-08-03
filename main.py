from situationController import controller


if __name__ == '__main__':
    cntrl=controller()
    user_input=input("What's your question?")
    cntrl.agent_selector(user_input)


