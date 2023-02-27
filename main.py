import sys 

def evaluateCommands(commandList):
    # Processing each command one by one.
    for command in commandList:
        commandType = command.split()[0]
        if(commandType == "CREATEHALL"):
            createHall(command)
        elif(commandType == "SELLTICKET"):
            sellAndCancel(command,True)
        elif(commandType == "CANCELTICKET"):
            sellAndCancel(command,False)
        elif(commandType == "BALANCE"):
            printBalance(command.split()[1:])
        elif(commandType == "SHOWHALL"):
            showHall(command.split()[1])

def createHall(command):
    # Using global keyword here to update halllist if all arguments are valid.
    global hallList
    # Using global keyword to be able to update the output string
    global output
    components = command.split()
    # Checking the number of arguments to validate all components.
    if len(components) < 3:
        output+="Error: Not enough parameters for creating a hall!\n"
        print("Error: Not enough parameters for creating a hall!")
        return
    elif len(components) > 3:
        output+= "Error: Too much parameters for creating a hall!\n"
        print("Error: Too much parameters for creating a hall!")
        return
    hallName = components[1]
    # Checking if hall is already created.
    if(checkHall(hallName=hallName)) :
        output+= "Warning: Cannot create the hall for the second time. The cinema has already {}\n".format(hallName)
        print("Warning: Cannot create the hall for the second time. The cinema has already {}".format(hallName))
        return
    rows = components[2].split("x")[0]
    if int(rows) > 26 or int(rows) < 1 :
        output+="Invalid argument for row value was entered!\n"
        print("Invalid argument for row value was entered!")
        return
    columns = components[2].split("x")[1]
    # Creating a dictionary to store all seats and setting all of them empty as default.
    seats = dict()
    for i in range(int(rows)):
        for j in range(int(columns)):
            seats[rowLetters[i]+str(j)] = "X"
    # Creating a new hall as a dictionary using appropriate keys.
    newHall = dict(name = hallName,rows=rows,columns=columns,seats=seats)
    hallList.append(newHall)
    output+="The hall ’{}’ having {} seats has been created.\n".format(hallName,int(rows)*int(columns))
    print("The hall ’{}’ having {} seats has been created.".format(hallName,int(rows)*int(columns)))


def checkHall(hallName):
    # Checking if the argument hall exists in the cinema.
    for hall in hallList:
        if hall.get("name") == hallName:
            return True
    return False

def sellAndCancel(command,operation):
    global hallList
    global output
    components = command.split()
    # Checking the command argument's validity.
    if len(components) < (5 if operation else 3):
        output+="Some arguments are missing! Please enter all necessary details.\n"
        print("Some arguments are missing! Please enter all necessary details.")
        return
    hallName = components[3 if operation else 1]
    if not checkHall(hallName=hallName):
        output+="There is no hall called {} in the cinema.\n".format(hallName)
        print("There is no hall called {} in the cinema.".format(hallName))
        return
    # Finding the hall and fetching its seats.
    hallIndex = findHall(hallName=hallName)
    hallSeats = hallList[hallIndex]["seats"]
    # Preparing the input seats. Number of seats can vary.
    inputSeats = components[4 if operation else 2:]
    for seat in inputSeats:
        # If seat is a range
        if "-" in seat:
            # Converting range to a list form.
            seatList = convertRange(seat)
            # Checking the validity of each seat in the range.
            validation = validateSeat(seatList,hallSeats,hallIndex,hallName)
            # If seats are validated and the operation is SELLTICKET
            if validation and operation:
                control = True
                # Checking the availability of each seat.
                for i in seatList:
                    if hallSeats[i] != "X":
                        output+= "Error: The seats {} cannot be sold to {} due some of them have already been sold!\n".format(seat,components[1])
                        print("Error: The seats {} cannot be sold to {} due some of them have already been sold!".format(seat,components[1]))
                        control = False
                        break
                # Updating status of the seats.
                if control:
                    for j in seatList:
                        hallList[hallIndex]["seats"][j] = components[2][0].upper()
                    output+= "Success: {} has bought {} at {}\n".format(components[1],seat,hallName)
                    print("Success: {} has bought {} at {}".format(components[1],seat,hallName))
            # If seats are validated and the operation is CANCELTICKET
            elif validation and not operation:
                control = True
                for i in seatList:
                    # If a seat is already available,no need to cancel it.
                    if hallSeats[i] == "X":
                        output+="Error: The seat {} at ’{}’ has already been free! Nothing to cancel\n".format(seat,hallName)
                        print("Error: The seat {} at ’{}’ has already been free! Nothing to cancel".format(seat,hallName))
                        control = False
                        break
                # Updating status of the seats.
                if control:
                    for j in seatList:
                        hallList[hallIndex]["seats"][j] = "X"
                    output+= "Success: The seats {} at ’{}’ have been canceled and now ready to be sold again\n".format(seat,hallName)
                    print("Success: The seats {} at ’{}’ have been canceled and now ready to be sold again".format(seat,hallName))
        
        # If input seat is not a range
        else:
            validation = validateSeat(seat,hallSeats,hallIndex,hallName)
            # If operation is SELLTICKET
            if validation and operation:
                control = True
                # If seat is not empty.
                if hallSeats[seat] != "X":
                    output+="Warning: The seat {} cannot be sold to {} since it was already sold!\n".format(seat,components[1])
                    print("Warning: The seat {} cannot be sold to {} since it was already sold!".format(seat,components[1]))
                    control = False
                    break
                if control:
                    # Selling the seat.
                    hallList[hallIndex]["seats"][seat] = components[2][0].upper()
                    output+="Success: {} has bought {} at {}\n".format(components[1],seat,hallName)
                    print("Success: {} has bought {} at {}".format(components[1],seat,hallName))
            ## If operation is CANCELTICKET
            elif validation and not operation:
                control = True
                # If seat is already empty.
                if hallSeats[seat] == "X":
                    output+= "Error: The seat {} at ’{}’ has already been free! Nothing to cancel\n".format(seat,hallName)
                    print("Error: The seat {} at ’{}’ has already been free! Nothing to cancel".format(seat,hallName))
                    control = False
                    break
                if control:
                    # Cancelling the ticket.
                    hallList[hallIndex]["seats"][seat] = "X"
                    output+="Success: The seat {} at ’{}’ have been canceled and now ready to be sold again\n".format(seat,hallName)
                    print("Success: The seat {} at ’{}’ have been canceled and now ready to be sold again".format(seat,hallName))
      
def findHall(hallName):
    # Searching the hallList and finding the index of the argument hall.
    hallIndex = 0
    for hall in hallList:
        if hall["name"] == hallName:
            return hallIndex
        hallIndex+=1

def printBalance(hallNames):
    global output
    # Printing the revenue report of the argument halls.
    for hallName in hallNames:
        # Finding the index of the hall.
        hallIndex = findHall(hallName)
        header = "Hall report of ’"+hallName+"’"
        # Fetching the seats of the hall. 
        hallSeats = hallList[hallIndex]["seats"]
        headerLength = len(header)
        numberOfStudents = 0
        numberOfFullFares = 0
        # Counting the students and full fares in the hall.
        for seat in hallSeats.keys():
            if hallSeats[seat] == "S":
                numberOfStudents+=1
            elif hallSeats[seat] == "F":
                numberOfFullFares+=1
        # Preparing the report.
        report = header+"\n"+"-"*headerLength+"\nSum of students = {}, Sum of full fares = {}, Overall = {}"
        output+= report.format(numberOfStudents*5,numberOfFullFares*10,(numberOfStudents*5)+(numberOfFullFares*10))+"\n"
        print(report.format(numberOfStudents*5,numberOfFullFares*10,(numberOfStudents*5)+(numberOfFullFares*10)))

def validateSeat(seat,allSeats,hallIndex,hallName):
    global output
    # Checking if seat specifies a range.
    if type(seat) is list:
        rowCheck = rowLetters.index(seat[0][0]) <= int(hallList[hallIndex]["rows"])-1
        if rowCheck:
            for s in seat:
                if s not in allSeats.keys():
                    # Checking if requested columns exist.
                    output+="Error: The hall ’{}’ has less column than the specified index {}!\n".format(hallName,seat[0]+"-"+seat[-1][1:])
                    print("Error: The hall ’{}’ has less column than the specified index {}!".format(hallName,seat[0]+"-"+seat[-1][1:])) 
                    return False
            return True
        # If program reaches here,it means the row name is invalid.
        output+="There is no row called {} in {}\n".format(seat[0][0],hallName)
        print("There is no row called {} in {}".format(seat[0][0],hallName))
        return False
    rowCheck = rowLetters.index(seat[0]) <= int(hallList[hallIndex]["rows"])-1
    # Checking the validity of the column indexes.
    if rowCheck:
        if seat in allSeats.keys():
            return True
        output+="The hall {} has less column than specified index {}\n".format(hallName,seat)
        print("The hall {} has less column than specified index {}".format(hallName,seat))
        return False
    output+="There is no row called {} in {}\n".format(seat[0],hallName)
    print("There is no row called {} in {}".format(seat[0],hallName))
    return False

def convertRange(seat):
    # Converting a seat range taken as a string to a list form.
    finalForm = list()
    split = seat.split("-")
    rowLetter = split[0][0]
    start = int(split[0][1])
    end = int(split[1])
    for i in range(start,end+1,1):
        finalForm.append(rowLetter+str(i))
    return finalForm

def showHall(hallName):
    # Visualizing the specified hall.
    global output
    hallIndex = findHall(hallName)
    # Fetching the necessary details of the hall.
    hall = hallList[hallIndex]
    seats = hall["seats"]
    rowCount = int(hall["rows"])
    columnCount = int(hall["columns"])
    visualization = ""
    # Using nested for loops to visualize the hall as 2D.
    for i in range(rowCount-1,-1,-1):
        rowName = rowLetters[i]
        visualization+= rowName+"  "
        for j in range(columnCount):
            seat = seats[rowName+str(j)]
            if j==columnCount-1:
                visualization+= seat+"\n"
                continue
            visualization+=seat+"  "
        if i==0:
            visualization+="   "
            for k in range(columnCount):
                if k<9:
                    visualization+=str(k)+"  "
                    continue
                visualization+=str(k)+" "
    output+=visualization+"\n"
    print(visualization)

# Getting the name of the input file from the argument list.
fileName = sys.argv[1]
output = ""
# Letters for the seats
rowLetters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
# Creating an empty list for storing all halls in the cinema.
hallList = list()

# Reading the lines of the input file and store them as a list.
with open(fileName,"r",encoding="utf-8") as input:
    commands = input.readlines()

# Sending all commands to evaluator function.
evaluateCommands(commands)

# Creating the output file.
with open("output.txt","w",encoding="utf-8") as outputFile:
    outputFile.write(output)


