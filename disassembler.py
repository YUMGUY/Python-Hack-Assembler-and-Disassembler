import re
import sys


compTableBackA0 = {'101010': '0', '111111': '1', '111010': '-1','001100': 'D', '110000': 'A', '001101':'!D',
                '110001': '!A','001111': '-D', '110011':'-A', '011111':'D+1', '110111': 'A+1', '001110':'D-1', '110010':'A-1'
                ,'000010':'D+A', '010011':'D-A', '000111':'A-D', '000000':'D&A','010101':'D|A' }

compTableBackA1 = {'101010': '0', '111111': '1', '111010': '-1','001100': 'D', '110000': 'M', '001101':'!D',
                '110001': '!M','001111': '-D', '110011':'-M', '011111':'D+1', '110111': 'M+1', '001110':'D-1', '110010':'M-1'
                ,'000010':'D+M', '010011':'D-M', '000111':'M-D', '000000':'D&M','010101':'D|M' }

destTableBack = {'000':'', '001':'M', '010':'D', '011': 'MD', '100': 'A', '101': 'AM', '110': 'AD'}

jumpTableBack = {'000':'','001':'JGT','010':'JEQ', '011': 'JGE', '100': 'JLT', '101': 'JNE', '110':'JLE', '111': 'JMP'}


# prompt for file name to disassemble
userInput = input("Enter the name of the hack file: ")
fileTranslated = open(userInput)


# writing to the output file, convert machine code to hack assembly code
userInputTranslated = userInput.replace('.hack','.asm')
disOutput = open(userInputTranslated, "w")

# reading a instruction
for line in fileTranslated:
    if(line.startswith('0')):
        #convert to positive integer
        line = int(line, 2) 

        #convert back to string
        line = str(line)
        disOutput.write('@' + line + "\n")
    
    elif(line.startswith('111')):
       # print('C instruction')

        aValue = line[3]
        comp = line[4:10]
        dest = line[10:13]
        jump = line[13:16]

        #just comp(op)
        if(jump == '000' and dest == '000'):

            if(aValue == '0'):
                convertedComp = compTableBackA0[comp]
            else:
                convertedComp = compTableBackA1[comp]
            
            convertedLine = convertedComp
            disOutput.write(convertedLine + "\n")
            continue

       # just dest = comp
        if(jump == '000'):
            convertedDest = destTableBack[dest]
            convertedJump = jumpTableBack[jump]
            if(aValue == '0'):
                convertedComp = compTableBackA0[comp]
            else:
                convertedComp = compTableBackA1[comp]
          
            convertedLine = convertedDest + '=' + convertedComp + convertedJump
            disOutput.write(convertedLine + "\n")
            continue


        # comp;jump
        if(dest == '000'):
            if(aValue == '0'):
                convertedComp = compTableBackA0[comp]
            else:
                convertedComp = compTableBackA1[comp]

            convertedJump = jumpTableBack[jump]
            convertedLine =  convertedComp + ';' + convertedJump
            disOutput.write(convertedLine + "\n")
            continue

        # dest = comp;jump
        if(aValue == '0'):
            convertedComp = compTableBackA0[comp]
        else:
            convertedComp = compTableBackA1[comp]
        
        if(not(dest == '000') and not(jump == '000')):
            
            convertedDest = destTableBack[dest]
            convertedJump = jumpTableBack[jump]
            convertedLine = convertedDest + '=' + convertedComp + ';' + convertedJump
            disOutput.write(convertedLine + "\n")
        
