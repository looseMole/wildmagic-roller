# Class that holds all info about a given table. For definition of a table, see the workbook.
class Table:
    # Initiate empty Table object
    def __init__(self, tableName, min=100, max=0) -> None:
        self.tableName = tableName
        self.min = min
        self.max = max
        self.outcomeArray = []

    # Add an outcome to the outcomeArray.
    def addOutcome(self, outcome):
        self.outcomeArray.append(outcome)
        self.updateBorderValues(outcome)

    def getOutcomeByDiceValue(self, diceValue):
        for i in range(len(self.outcomeArray)):
            if self.outcomeArray[i].min <= diceValue <= self.outcomeArray[i].max:
                return self.outcomeArray[i].getOutput()

    # Updates the bordervalues self.min and self.max, if the given outcome has a greater/lesser max/min value.
    def updateBorderValues(self, outcome):
        if outcome.getMax() > self.max:
            self.max = outcome.getMax()
        if outcome.getMin() < self.min:
            self.min = outcome.getMin()

    def getMin(self):
        return self.min

    def getMax(self):
        return self.max

    # Overrides the default tostring method.
    def __str__(self):
        tableString = f"{self.tableName}, with a min of {self.min} and a max of {self.max}, " \
                      f"has the following outcomes: "
        for i in range(len(self.outcomeArray)):
            tableString += str(self.outcomeArray[i])
        return tableString
