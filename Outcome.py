class Outcome:
    min = 0
    max = 100
    output = "N/A"
    goToTable = 0
    goToExceptions = {}

    def __init__(self, min, max, output, goToTable=0, goToExceptions=0):
        self.min = min
        self.max = max
        self.output = output
        self.goToTable = goToTable
        self.goToExceptions = goToExceptions

    def getOutput(self):
        return self.output

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
