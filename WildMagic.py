import random
import sys
import openpyxl
from openpyxl import DEFUSEDXML
import os
from platform import system
from Table import Table
from Outcome import Outcome

# TODO: Add more comments!
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


# A recursive method for executing goTo functionality.
recursionCounter = 0  # Is incremented inside the method. If too large, the spreadsheet probably has a goTo-Loop.
recursionLimit = settingSheet['B2'].value
warningHasBeenPrinted = False


def executeOutcome(outcome):
    global recursionCounter, recursionLimit
    global tableArray
    global warningHasBeenPrinted
    stop = False

    while not stop and recursionCounter < recursionLimit:
        if outcome.hasGoTo():
            tableIndex = -1  # Initialization of tableIndex.

            for string in outcome.getGoToTableArray():
                # Find table mentioned in goTo:
                for i in range(len(tableArray)):
                    if tableArray[i].getName().replace(" ", "") == string:  # If a tablename matches the input string
                        tableIndex = i
                        break

                if tableIndex == -1:  # If tableIndex has not been changed, no valid table has been found.
                    raise Exception("Name in GoTo-cell not valid.")

                # Rolls on the found table.
                print(f"Rolling on {tableArray[tableIndex].getName()}...")

                # TODO: Remake this, to use diceRoll()s exception-support.
                rollIsValid = False
                rollAttempts = 0  # If more than 100 attempts is needed to get a valid roll, it is probably impossible.
                while (not rollIsValid and rollAttempts < 100):
                    roll = diceRoll(tableArray[tableIndex].getMin(), tableArray[tableIndex].getMax())
                    rollAttempts += 1

                    # Check whether given roll is marked in the "except"-column.
                    if roll in outcome.getSingleException():
                        continue
                    else:
                        rollInRange = False  # Initialization, in case the first roll works.
                        for exceptRange in outcome.getRangeException():
                            rollInRange = False
                            if int(exceptRange[0]) <= roll <= int(exceptRange[1]):
                                rollInRange = True
                        if (rollInRange):
                            continue

                    # If roll has not appeared in either of the exception arrays, accept the roll.
                    rollIsValid = True

                if (not rollIsValid):
                    print("Could not, with 1000 tries, get a valid roll.")
                    return

                # Prints result of roll to console.
                print(f"Rolled a {roll}...")
                newOutcome = tableArray[tableIndex].getOutcomeByDiceValue(roll)
                print(newOutcome.getOutput()+"\n")

                # Note: Recursion
                # Tries to call this method again. If new outcome has no GoTo reference, stop will be set to True, and
                # the recursive loop will end.
                recursionCounter += 1
                print(recursionCounter)
                stop = executeOutcome(newOutcome)  # If True, the loop is ended.

        else:  # If outcome has no goTo:
            stop = True

    if recursionCounter >= recursionLimit and not warningHasBeenPrinted:
        print(f"Warning: Program has now rolled on a table {recursionCounter} times. It seems there is a goTo loop.")
        print(f"Aborting execution, as number of rolls without input has been set to {recursionLimit} in settings.")
        warningHasBeenPrinted = True
    return True  # If the condition reached this far, return True to end recursive loop.


# Map the tables into Table and Outcome objects #
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
    # Create the table.
    currTable = Table(diceSheet["A" + str(minCellRow - 1)].value)  # Reads the name from the corner of the table.
    tableArray.append(currTable)

    # Create the tables first Outcome object, and add it to the table.
    if diceSheet[minCell].value and diceSheet[maxCell].value and diceSheet[outputCell].value:
        currOutcome = Outcome(diceSheet[minCell].value, diceSheet[maxCell].value, diceSheet[outputCell].value, diceSheet[goToCell].value, diceSheet[exceptCell].value)
        tableArray[len(tableArray)-1].addOutcome(currOutcome)
    else: # TODO: Add isFirstTable check here, as to only break if no tables can be made.
        raise Exception(f"Table found with wrong or no outcome values, on row {minCellRow}.")

    # Add the rest of the Outcomes (which should have no more than one empty row between them.)
    while emptyRow < 1:
        incrementCellRows(3)
        if diceSheet[minCell].value and diceSheet[maxCell].value and diceSheet[outputCell].value:
            currOutcome = Outcome(diceSheet[minCell].value, diceSheet[maxCell].value, diceSheet[outputCell].value, diceSheet[goToCell].value, diceSheet[exceptCell].value)
            tableArray[len(tableArray)-1].addOutcome(currOutcome)
            emptyRow = 0
        else:
            emptyRow += 1

    # Checks whether the spreadsheet has more tables following the current one, and if so, starts the loop over with
    # that Table.
    incrementCellRows(2)
    if diceSheet[minCell].value and diceSheet[maxCell].value and diceSheet[outputCell].value:
        emptyRow = 0
        continue
    else:
        emptyRow += 1

# Execution part:
startTableIndex = 0  # By default, the first index in the tableArray houses the main/start table.
isTableName = False

# Check for parameters passed, when calling program, and whether said parameter is a valid tablename.
if (len(sys.argv) - 1):
    # Check whether parameter is a valid Table name.
    for i in range(len(tableArray)):
        if tableArray[i].getName() == sys.argv[1]:
            isTableName = True
            startTableIndex = i
            break
    if not isTableName:  # Will evaluate to True if given parameter is a valid Table name.
        nameArray = []
        for table in tableArray:
            nameArray.append(table.getName())
        print(f"Invalid input \"{sys.argv[1]}\". Valid inputs are: {nameArray}.")
        exit()

# Initial table roll:
# Roll on the table defined as main (default is the first table in the spreadsheet)
print(f"Rolling on {tableArray[startTableIndex].getName()}...")
roll = diceRoll(tableArray[startTableIndex].getMin(), tableArray[startTableIndex].getMax())
print(f"Rolled a {roll}...")
outcome = tableArray[startTableIndex].getOutcomeByDiceValue(roll)
print(outcome.getOutput()+"\n")

# Following table rolls:
executeOutcome(outcome)
