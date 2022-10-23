import random
import openpyxl
from openpyxl import DEFUSEDXML
import os
from platform import system
from Table import Table
from Outcome import Outcome

# Global variables
scriptFolder = os.path.dirname(__file__)
if system() == 'Windows':
    folderIndicator = '\\'
else:
    folderIndicator = '/'
workbook = openpyxl.load_workbook(scriptFolder+f"{folderIndicator}customDiceOutcomes.xlsx")
diceSheet = workbook.active
settingSheet = workbook["settings"]

# Double-checking DEFUSEDXML being active
if not DEFUSEDXML:
    print("Please install and setup DEFUSEDXML")


# Takes a string as arg, returns int or float
def strToNum(string):
    if isinstance(string, bool):
        return string
    try: # Try to turn the input into an int. If not possible, try turning into float.
        return int(string)
    except ValueError or TypeError:
        print("Value could not be converted to int")
        try:
            return float(string)
        except TypeError:
            return


# "Rolls the dice" between a given min, and max. Re-rolls if result is contained in the array of exceptions.
def diceRoll(min=1, max=100, exceptions=[]):
    result = random.randint(min, max)
    while result in exceptions:
        result = random.randint(min, max)
    return result


def incrementCellRows(amount):
    global minCellRow, maxCellRow, minCell, maxCell, outputCell, goToCell, exceptCell
    minCellRow += amount
    maxCellRow = minCellRow + 1
    minCell = "B" + str(minCellRow)
    maxCell = "B" + str(maxCellRow)
    outputCell = "C" + str(minCellRow)
    goToCell = "D" + str(minCellRow)
    exceptCell = "E" + str(minCellRow)


# Map the tables into Table and Outcome objects.
tableArray = []

minCellRow = 2  # Start at two per default spreadsheet. max-, outcome, GoTo, and Except-cells are at this row as well.
maxCellRow = minCellRow + 1

minCell = "B" + str(minCellRow)
maxCell = "B" + str(maxCellRow)
outputCell = "C" + str(minCellRow)
goToCell = "D" + str(minCellRow)
exceptCell = "E" + str(minCellRow)

# Counter for amount of empty rows encountered. If an empty row has been met once the table is assumed ended.
emptyRow = 0
while emptyRow < 2:
    # Create the first table and if default starting line for table values is not empty, add the first outcome.
    currTable = Table(diceSheet["A" + str(minCellRow - 1)].value)  # Reads the name from the corner of the table.
    tableArray.append(currTable)

    if diceSheet[minCell].value and diceSheet[maxCell].value and diceSheet[outputCell].value:
        currOutcome = Outcome(diceSheet[minCell].value, diceSheet[maxCell].value, diceSheet[outputCell].value)
        tableArray[len(tableArray)-1].addOutcome(currOutcome)
    else:
        exit()

    while emptyRow < 1:
        incrementCellRows(3)
        # print(minCell)
        if diceSheet[minCell].value and diceSheet[maxCell].value and diceSheet[outputCell].value:
            currOutcome = Outcome(diceSheet[minCell].value, diceSheet[maxCell].value, diceSheet[outputCell].value)
            tableArray[len(tableArray)-1].addOutcome(currOutcome)
            emptyRow = 0
        else:
            emptyRow += 1

    incrementCellRows(2)
    if diceSheet[minCell].value and diceSheet[maxCell].value and diceSheet[outputCell].value:
        emptyRow = 0
        continue
    else:
        emptyRow += 1
