import customtkinter 

class Quiz:
    def __init__(self, fact_1, fact_2, fact_3, fact_4):
        self.fact_1 = fact_1
        self.fact_2 = fact_2
        self.fact_3 = fact_3
        self.fact_4 = fact_4

    def fact_btn_1(self):
        self.fact_1 = customtkinter.CTkButton()
    