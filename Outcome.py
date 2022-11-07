# TODO: Make functionality for parsing input from goTo and Except cells to something useful.
class Outcome:
    def __init__(self, min, max, output, goToTable='', goToExceptions=''):
        # self.min = 0
        # max = 100
        # output = "N/A"
        # goToTableArray = []
        self.singleException = []
        self.rangeException = []

        self.min = min
        self.max = max
        self.output = output
        # Turns the goToTable input from a str to a list of Table names.
        if isinstance(goToTable, str):
            goToTable = goToTable.replace(" ", "")
            goToTable = goToTable.split(",")
            self.goToTableArray = goToTable
        # Turns the goToExceptions input from a str to either a list of min-max pairs, or a list of single ints.
        if goToExceptions:
            goToExceptions = goToExceptions.replace(" ", "")
            goToExceptions = goToExceptions.split(",")
            for exception in goToExceptions:
                if exception.__contains__('-'):
                    exception = exception.split("-")
                    self.rangeException.append(exception)  # Note: Each element is array of 2 strings.
                else:
                    self.singleException.append(int(exception))  # Notes: Each element is int.

    def hasGoTo(self):
        if self.goToTableArray:
            return True
        else:
            return False

    def hasExceptions(self):
        if self.singleException or self.rangeException:
            return True
        else:
            return False

    def getOutput(self):
        return self.output

    def getMin(self):
        return self.min

    def getMax(self):
        return self.max

    def getGoToTableArray(self):
        return self.goToTableArray

    def getSingleException(self):
        return self.singleException

    def getRangeException(self):
        return self.rangeException

    # Overriding native tostring method for Outcome
    def __str__(self):
        outcomeString = f"\n\"{self.output}\":\nmin: {self.min}\nmax: {self.max}"

        if self.goToTable != 0:
            outcomeString += f"\nRoll again, on table: {self.goToTable}"
            if not len(self.goToExceptions) == 0:  # If there are rolls which needs to be ignored, when rolling again
                outcomeString += ", ignoring "
                for i in range(len(self.goToExceptions)):  # Adding all values from the exceptions list, appending ','
                    # -if there are more items left to print.
                    outcomeString += f"{str(self.goToExceptions[i])}"
                    if not i == len(self.goToExceptions):
                        outcomeString += ", "
        return outcomeString
