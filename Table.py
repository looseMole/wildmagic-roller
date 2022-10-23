# Class that holds all info about a given table. For definition of a table, see the workbook.
class Table:
    min = 0
    max = 100
    tableName = ""

    # Initiate empty Table object
    def __init__(self, tableName, min=0, max=0) -> None:
        self.tableName = tableName
        self.min = min
        self.max = max
        self.outcomeArray = []

    # Add an outcome to the outcomeArray.
    def addOutcome(self, outcome):
        self.outcomeArray.append(outcome)

    def getOutcomeByDiceValue(self, diceValue):
        for i in range(len(self.outcomeArray)):
            if self.outcomeArray[i].min <= diceValue <= self.outcomeArray[i].max:
                return self.outcomeArray[i].getOutput()

    def load(self, startingCell):
        pass

    # Overrides the default tostring method.
    def __str__(self):
        tableString = f"{self.tableName}, with a min of {self.min} and a max of {self.max}, " \
                      f"has the following outcomes: "
        for i in range(len(self.outcomeArray)):
            tableString += str(self.outcomeArray[i])
        return tableString
