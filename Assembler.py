
import re
import sys

# making symbol table
def createSymbolTable(asmFileNam):
    # predefined symbols
    symbolTable =  {'RO': 0, 'R1' : 1, 'R2': 2, 'R3': 3, 'R4': 4,'R5': 5, 'R6': 6, 'R7': 7,'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
                   'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SP': 0,
                   'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'SCREEN': 16384,
                   'KBD': 24576}

    fileSymbol = open(asmFileNam)
    pcCounter = 0
    for line in fileSymbol:
        if(line == "" or line == "\n"):
           # print('ignore this line')
            continue
        if(line.startswith('/')):
            continue
        #take out side comments
        if('//' in line):
            sideCom = line.find('//')
            li = line[:sideCom]
            line = li

        cleanLine = line.strip()
        # a label
        if(cleanLine.startswith('(')):
            cleanLine = re.sub(r'[()]','',cleanLine)
            if(cleanLine not in symbolTable):
                symbolTable[cleanLine] = pcCounter
               # print(str(pcCounter) + ' with ' + cleanLine)
        
        if(isAInstructionQual(cleanLine) or isCInstructionQual(cleanLine)):
            if(line.startswith('(')):
               # print('is label')
                continue
            else:
                #print(str(pcCounter) + ' with ' + cleanLine)
                pcCounter = pcCounter + 1
                
            continue
           # print(str(pcCounter) + ' with ' + cleanLine)

    fileAsymbol = open(asmFileNam)
    nextAddress = 16
    for line in fileAsymbol:
        cleanA = line.strip()

        if(cleanA.startswith('@')):

            # take out side comment
            if('//' in cleanA):
                #print('found side comment')
                sideIndex = cleanA.find('//')
                cl = cleanA[:sideIndex]
                cleanA = cl.strip()

            aInstruction = cleanA.strip('@')
            # check if the a instruction variable is not in the symbol table yet
            if(not aInstruction.isdigit() and aInstruction not in symbolTable):
                #print(aInstruction + "not in here\n")
                symbolTable[aInstruction] = nextAddress
                nextAddress = nextAddress + 1

    return symbolTable

# making comp table

def createCompTable():
    computationTable = {'0': '101010', '1': '111111', '-1': '111010', 'D': '001100',
               'A': '110000', '!D': '001101', '!A': '110001', '-D': '001111',
               '-A': '110011', 'D+1': '011111', 'A+1': '110111',
               'D-1': '001110', 'A-1': '110010', 'D+A': '000010',
               'D-A': '010011', 'A-D': '000111', 'D&A': '000000',
               'D|A': '010101', 'M': '110000', '!M': '110001', '-M': '110011',
               'M+1': '110111', 'M-1': '110010', 'D+M': '000010',
               'D-M': '010011', 'M-D': '000111', 'D&M': '000000',
               'D|M': '010101'}    


    return computationTable

def createDestTable():
    destinationTable = {'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101',
                       'AD': '110', 'AMD': '111'} 

    return destinationTable

def createJumpTable():
    jumpTABLE = {'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101',
         'JLE': '110', 'JMP': '111'}
    return jumpTABLE


def isAInstructionQual(line):
    
    if(not (line.startswith('@'))):
        return False
    
    #then if it does have @
    # if it's a number
    cleanedLine = line[1:len(line)]

    if(cleanedLine.isdigit() and int(cleanedLine) >= 0):
        return True

    if(cleanedLine[0].isdigit()):
        return False
    else:
        return True
    
    return False


def isCInstructionQual(line):
    line = line.replace(' ', "")
    tokensQ = re.split('=|;', line)
    if(len(tokensQ) == 1):
        #print('sole op')
        return True
    if(not(line.count('=') == 1 or line.count(';') == 1)):
        #print(line +' was not c instruction')
        return False

    return True

def convertCInstruction(line):
    line = line.replace(' ', "")
    tokens = re.split('=|;', line)
    #print(tokens)
    prefixInstruction = '111'

    destination = ''
    comp = ''
    jump = ''
    a = ''

    if(len(tokens) == 2): # dest and comp in the line
     
        if(line.count('=') == 1):
            destination = destTable[tokens[0]]
           # print(destination + ' is the dest')
            comp = compTable[tokens[1]]
            #print(comp + ' is the comp')
            jump = "000"

            if('M' in tokens[1]):
                a = '1'
            else:
                a = '0'

        #comp and jump in the line
        elif(line.count(';') == 1):
            
            destination = "000"
            comp = compTable[tokens[0]]
           # print(comp + " is the comp2")
            jump = jumpTable[tokens[1]]
           # print(jump + " is the jump")
            if('M' in tokens[0]):
                a = '1'
            else:
                a = '0'

    # only op is in the line
    elif(len(tokens) == 1):
            destination = '000'
            comp = compTable[tokens[0]]
           # print(comp + ' is the comp alone')
            jump = '000'
            if('M' in tokens):
                a = '1'
            else:
                a = '0'
    

    # it is dest = comp;jump
    else:
        destination = destTable[tokens[0]]
        comp = compTable[tokens[1]]
        jump = jumpTable[tokens[2]]
        if('M' in tokens[1]):
            a = '1'
        else:
            a = '0'

        

    return (prefixInstruction + a + comp + destination + jump)


# start of program
userinput = input("Enter the file: ")
symbolTable = createSymbolTable(userinput)
compTable = createCompTable()
destTable = createDestTable()
jumpTable = createJumpTable()


# main program
# checking for errors


file = open(userinput)
userinput = userinput.replace('.asm', '.hack')

binaryFile = open(userinput,"w")


# for testing
for line in file:
   
    # take out side comments
    if('//' in line):
        sideComindex = line.find('//')
        line = line[:sideComindex]
    line = line.strip()
    
    if(line.startswith('/')):
        continue
    # if it's a label, dont count it
    if(line.startswith('(')):
        continue

    if(line == ""): 
        continue

    if(isAInstructionQual(line)):
        droppedAt = line[1:len(line)]

        # check if it's a number
        if(droppedAt.isdigit()):
            converted = '0' + format(int(droppedAt),'015b')
            binaryFile.write(converted + "\n")
            continue

        converted = '0' + format(symbolTable[droppedAt],'015b') # machine code output
        #print(str(symbolTable[droppedAt]) + ' with ' + droppedAt)
        binaryFile.write(converted + "\n") # to separate the lines
        continue
    
    
    #know for sure that it is a C instruction
    if(isCInstructionQual(line)):
        cinst = convertCInstruction(line)
        binaryFile.write(cinst + "\n")
    #binaryFile.write(line)


binaryFile.close()
file.close()