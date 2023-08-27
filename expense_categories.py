class ExpenseCategory:
    def __init__(self, name, description="", budget=0):
        self.name = name
        self.desctiption = description
        self.budget = budget
        self.expenses = []