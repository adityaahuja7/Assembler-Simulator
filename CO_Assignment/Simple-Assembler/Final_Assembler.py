import sys
import re
#global variables
Assembly_Input = []  # raw input
Instructions = []  # only instructions in asm form
variables = []  # variables name are saved here
Labels = {}  # labels are saved here , Key: Value= Label_Name: Line Number
Binary_Output = []  # Output of binary if there is no error
toPrint = True  # Check if error, if no error then we print binary output
# Sets to true when we first encounter the first normal instruction
First_Variable = False
Hlt_Handle = False  # Sets to true at the first instance of halt instruction

# Registers in decimal for execution
R0 = 0
R1 = 0
R2 = 0
R3 = 0
R4 = 0
R5 = 0
R6 = 0
flag = 0

# Mapping to connect string to decimal
Registers = {
    "R0": R0,
    "R1": R1,
    "R2": R2,
    "R3": R3,
    "R4": R4,
    "R5": R5,
    "R6": R6,
    "FLAGS": flag
}

# Length of different instruction types
OpLen = {
    "add": 4, "mul": 4, "sub": 4, "xor": 4, "or": 4, "and": 4,
    "rs": 3, "ls": 3, "mov": 3,
    "div": 3, "not": 3, "cmp": 3,
    "ld": 3, "st": 3,
    "jmp": 2, "jlt": 2, "jgt": 2, "je": 2,
    "hlt": 1,
    "var": 2
}

# Typecodes of the instructions, i.e switching between string and instruction type
OpType = {
    "add": "A", "mul": "A", "sub": "A", "xor": "A", "or": "A", "and": "A",
    "rs": "B", "ls": "B", "mov": "B",
    "div": "C", "not": "C", "cmp": "C",
    "ld": "D", "st": "D",
    "jmp": "E", "jlt": "E", "jgt": "E", "je": "E",
    "hlt": "F",
    "var":"ignore"
}

# Binary translation of different instruction types
OpBin = {
    "add": "00000", "mul": "00110", "sub": "00001", "xor": "01010", "or": "01011", "01100": "A",
    "movB": "00010", "rs": "01000", "ls": "01001",
    "movC": "00011", "div": "00111", "not": "01101", "cmp": "01110",
    "ld": "00100", "st": "00101",
    "jmp": "01111", "jlt": "1000", "jgt": "10001", "je": "10010",
    "hlt": "10011"
}

# Binary translation of diffirent registers
RegBin = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111"
}


def GetBinary(Cur):
    # Gets the binary of an entire instruction and returns it.
    BinOut = ""
    # the instruction is broken into a list of components
    temp = Cur[1].split()
    if (temp[0] == "add"):
        BinOut += OpBin["add"]
        BinOut += "00"
        BinOut += RegBin[temp[1]]
        BinOut += RegBin[temp[2]]
        BinOut += RegBin[temp[3]]

    if (temp[0] == "sub"):
        BinOut += OpBin["sub"]
        BinOut += "00"
        BinOut += RegBin[temp[1]]
        BinOut += RegBin[temp[2]]
        BinOut += RegBin[temp[3]]

    if (temp[0] == "mul"):
        BinOut += OpBin["mul"]
        BinOut += "00"
        BinOut += RegBin[temp[1]]
        BinOut += RegBin[temp[2]]
        BinOut += RegBin[temp[3]]

    if (temp[0] == "xor"):
        BinOut += OpBin["xor"]
        BinOut += "00"
        BinOut += RegBin[temp[1]]
        BinOut += RegBin[temp[2]]
        BinOut += RegBin[temp[3]]

    if (temp[0] == "or"):
        BinOut += OpBin["or"]
        BinOut += "00"
        BinOut += RegBin[temp[1]]
        BinOut += RegBin[temp[2]]
        BinOut += RegBin[temp[3]]

    if (temp[0] == "and"):
        BinOut += OpBin["add"]
        BinOut += "00"
        BinOut += RegBin[temp[1]]
        BinOut += RegBin[temp[2]]
        BinOut += RegBin[temp[3]]

    if (temp[0] == "rs"):
        BinOut += OpBin["rs"]
        BinOut += RegBin[temp[1]]
        BinVal = int(temp[2][1:])
        BinVal = ('{0:08b}'.format(BinVal))  # We are turning
        BinOut += BinVal

    if (temp[0] == "mov"):

        if(temp[2][0] == '$'):
            BinOut += OpBin["movB"]
            BinOut += RegBin[temp[1]]
            BinVal = int(temp[2][1:])
            BinVal = ('{0:08b}'.format(BinVal))
            BinOut += BinVal

        elif (temp[2][0] != "$"):
            BinOut += OpBin["movC"]
            BinOut += "00000"
            BinOut += RegBin[temp[1]]
            BinOut += RegBin[temp[2]]

    if (temp[0] == "ls"):
        BinOut += OpBin["ls"]
        BinOut += RegBin[temp[1]]
        BinVal = int(temp[2][1:])
        BinVal = ('{0:08b}'.format(BinVal))
        BinOut += BinVal

    if (temp[0] == "div"):
        BinOut += OpBin["div"]
        BinOut += "00000"
        BinOut += RegBin[temp[1]]
        BinOut += RegBin[temp[2]]

    if (temp[0] == "not"):
        BinOut += OpBin["not"]
        BinOut += "00000"
        BinOut += RegBin[temp[1]]
        BinOut += RegBin[temp[2]]

    if (temp[0] == "cmp"):
        BinOut += OpBin["cmp"]
        BinOut += "00000"
        BinOut += RegBin[temp[1]]
        BinOut += RegBin[temp[2]]

    if (temp[0] == "ld"):
        BinOut += OpBin["ld"]
        BinOut += RegBin[temp[1]]
        BinOut += ('{0:08b}'.format(variables[temp[2]]))

    if (temp[0] == "st"):
        BinOut += OpBin["st"]
        BinOut += RegBin[temp[1]]
        BinOut += ('{0:08b}'.format(variables[temp[2]]))

    if (temp[0] == "jmp"):
        BinOut += OpBin["jmp"]
        BinOut += "000"
        BinOut += ('{0:08b}'.format(Labels[temp[1]]))

    if (temp[0] == "jlt"):
        BinOut += OpBin["jlt"]
        BinOut += "000"
        BinOut += ('{0:08b}'.format(Labels[temp[1]]))

    if (temp[0] == "jgt"):
        BinOut += OpBin["jgt"]
        BinOut += "000"
        BinOut += ('{0:08b}'.format(Labels[temp[1]]))

    if (temp[0] == "je"):
        BinOut += OpBin["je"]
        BinOut += "000"
        BinOut += ('{0:08b}'.format(Labels[temp[1]]))

    if (temp[0] == "hlt"):
        BinOut = OpBin["hlt"]+"00000000000"

    return BinOut


def CheckOverflow(val):
    return val < 0 or val > 255


def assemble():
    for i in Instructions:
        try:
            BinString = GetBinary(i)
            Binary_Output.append(BinString)
            
        except:
            toPrint = False
            print("ERROR: Wrong syntax used for instructions")
            break


def printBinary():
    for i in Binary_Output:
        print(i)


def ConvertToBinary(dec_val):
    binval = ('{0:016b}'.format(dec_val))
    return binval


def parser(command):
    return command.split()


def LabelCheck(LabelName):
    if re.match(r'^\w+$', LabelName):
        return True
    else:
        return False


def checkSyn(com):
    return com in Registers.keys() or com in OpType.keys() or (com[0] == "$" and not com[1:].isalpha()) or com[len(com)-1] == ":" or com == "var"


def error():
    global First_Variable, Hlt_Handle
    try:
        for line, inst in Assembly_Input:
            if (len(inst) == 0):
                continue

            # stores the instruction corresponding to a label
            elif (inst[0][len(inst[0])-1] == ":"):
                x = inst[0][:len(inst[0])-1]
                ins = inst[1:]
                if (LabelCheck(x) == False):
                    print("ERROR: Label name is in correct in line:", line)
                    return False

            else:
                ins = inst

            if (checkSyn(ins[0]) and OpLen[ins[0]] != len(ins)):
                print("ERROR: General Syntax error in line:", line)
                return False
            
            # halt error handling for multiple halts and halt not being used as last 
            if (ins[0] == "hlt"):
                if (Hlt_Handle == False):
                    Hlt_Handle = True
                else:
                    print("ERROR: Multiple halt instructions being used at line:", line)
                    return False
            else:
                if (Hlt_Handle == True):
                    print("ERROR: Halt instruction is not the last instruction at line:", line)
                    return False

            if (ins[0] == "var"):
                if (LabelCheck(ins[1]) == False):
                    print("ERROR: variable name is incorrect in line:", line)
                    return False
                if (First_Variable == True):
                    print("ERROR: Variables not being declared in the beginning at:", line)
                    return False
                continue
                
            elif (ins[0] != "var"):
                if (First_Variable == False):
                    First_Variable = True
                

            # check Syntax Error
            if (checkSyn(ins[0]) and OpType[ins[0]] == "E"):
                if (not checkSyn(ins[0])):
                    print("ERROR: Syntax error in instruction name or register name in line:", line)
                    return False

            elif (checkSyn(ins[0]) and OpType[ins[0]] == "D"):
                if not checkSyn(ins[0]) or not checkSyn(ins[1]):
                    print("ERROR: Syntax error in instruction name or register name in line:", line)
                    return False

            else:
                for t in ins:
                    if (not checkSyn(t)):
                        print("ERROR: Syntax error in instruction name or register name in line:", line)
                        return False

            # check undefined variable
            if (OpType[ins[0]] == "D"):
                if (ins[2] not in variables.keys()):
                    print("ERROR: Use of undefined variable in line:", line)
                    return False

            # check undefined label
            if (OpType[ins[0]] == 'E'):
                if (ins[1] not in Labels.keys()):
                    print("ERROR: Use of undefined label in line:", line)
                    return False

            # check illegal flag use
            if (ins[0] != "mov"):
                if "FLAGS" in ins:
                    print("ERROR: Illegal use of FLAG register in line:", line)
                    return False

            # illegal immediate value
            if (OpType[ins[0]] == "B" and ins[2] not in Registers.keys()):
                if(CheckOverflow(int(ins[2][1:]))):
                    print("ERROR: Overflow error in line:", line)
                    return False

            # misuse of variables/labels
            if (OpType[ins[0]] == "D"):
                if (ins[1] in Labels.keys()):
                    print("ERROR: Misuse of variable as flag in line:", line)

            elif (OpType[ins[0]] == "E"):

                if (ins[1] in variables.keys()):
                    print("ERROR: Misuse of flag as variable in line:", line)

    except ():
        print("Error: General Syntax error in line:", line)
        return False
    # Check to see if there is any halt instruction at all
    if (Hlt_Handle == False):
        print("ERROR: Halt handle instruction has not been used")
        return False
    return True


def read():
    global Assembly_Input, Instructions, variables, Labels
    line = 0
    temp = ""
    Label_Flag=True
    var_count=0
    try:
        while (True):
            temp = input().lstrip()
            Assembly_Input.append(temp.split())
            if (temp != ""):
                Typecheck = temp.split(" ")
                if (Typecheck[0] == "var" and len(Typecheck)>1):
                    variables.append(Typecheck[1])
                    var_count+=1

                elif (Typecheck[0][len(Typecheck[0])-1] == ":"):
                    if (Typecheck[0][0:len(Typecheck[0])-1] in list(Labels.keys())):
                        Label_Flag=False
                    Labels[Typecheck[0][0:len(Typecheck[0])-1]] = line
                    Instructions.append(temp[(len(Typecheck[0])+1):])

                else:
                    Instructions.append(temp)
            line += 1
    
    except (EOFError):
        Assembly_Input = list(enumerate(Assembly_Input, start=1))
        Instructions = list(enumerate(Instructions, start=0))
        variables = dict(list(enumerate(variables, start=len(Instructions))))
        variables = {v: k for k, v in variables.items()}

    for i in Labels:
        Labels[i]-=var_count

    if (Label_Flag==False):
            print("ERROR: multiple labels with same name")
    else:
        if (error()):
            assemble()
        if (toPrint):
            printBinary()

read()