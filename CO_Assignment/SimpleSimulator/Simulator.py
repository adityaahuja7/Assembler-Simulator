#Registers and flags
flag = 0
Registers = [0, 0, 0, 0, 0, 0, 0]

# mapping of program counter and memory address
pc_and_mem = []


OpCode = {"00000": "add", "00001": "sub", "00010": "movI", "00011": "movR", "00100": "load",
          "00101": "st", "00110": "mul", "00111": "div", "01000": "rs", "01001": "ls",
          "01010": "xor", "01011": "or", "01100": "and", "01101": "inv", "01110": "cmp", "01111": "jmp",
          "10000": "jlt", "10001": "jgt", "10010": "je", "10011": "halt"}
Instructions = []
Memory_Heap=[]
pc = 0
cycle = 0


def checkOverflow():
    global Registers, flag
    for i in range(0, len(Registers)):
        if (Registers[i] > 255 or Registers[i] < 0):
            Registers[i] = 0
            flag += 8
    return

# framework
#


def flag_reset(): #resets flag do use this wherever necessary
    global flag
    flag = 0
    return


def ConvertToBinary16(dec_val):
    binval = ('{0:016b}'.format(dec_val))
    return binval


def ConvertToBinary8(dec_val):
    binval = ('{0:08b}'.format(dec_val))
    return binval

def ConvertToDecimal(bin_val):
    return int(bin_val, 2)


def outputOneLine():
    print("trolls3XOx")  # temporary print statement

# 8 bit address and returns a 16 bit value as the data, 512 bytes stores 0 se initialized


def memory(instruction):
    pass

def initializeMem():
    for i in range(0,256):
        Memory_Heap[i]=0
    return
#     # i = [00001010101, 01001001001, 01001010101]


# def program_counter:  # 8bit register that points to the current instruction



# operations
def add(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)]+Registers[ConvertToDecimal(reg2)]
    checkOverflow()
    return

def sub(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)]-Registers[ConvertToDecimal(reg2)]
    checkOverflow()
    return

def mul(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] * Registers[ConvertToDecimal(reg2)]
    checkOverflow()
    return

def xor(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] ^ Registers[ConvertToDecimal(reg2)]
    return

def BITor(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] | Registers[ConvertToDecimal(reg2)]
    return

def BITand(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] & Registers[ConvertToDecimal(reg2)]
    return

def rs(instruction):
    to_store = instruction[0:3]
    value = ConvertToDecimal(instruction[3:])

    Registers[ConvertToDecimal(
        to_store)] = Registers[ConvertToDecimal(to_store)] // (2**value)
    return

def ls(instruction):
    to_store = instruction[0:3]
    value = ConvertToDecimal(instruction[3:])

    Registers[ConvertToDecimal(
        to_store)] = Registers[ConvertToDecimal(to_store)] * (2**value)
    if (Registers[ConvertToDecimal(to_store)]>255):
        Registers[ConvertToDecimal(to_store)]=0
    return

def movI(instruction):
    to_store = instruction[0:3]
    value = ConvertToDecimal(instruction[3:])

    Registers[ConvertToDecimal(
        to_store)] = value
    return

def movR(instruction):
    global flag
    to_store = instruction[0:3]
    reg_aux = ConvertToDecimal(instruction[3:])
    if (reg_aux == 7):
        Registers[ConvertToDecimal(
            to_store)]=flag
    else:
        Registers[ConvertToDecimal(
            to_store)] = Registers[reg_aux].copy()
    return
    
def div(instruction):
    rega = ConvertToDecimal(instruction[0:3])
    regb = ConvertToDecimal(instruction[3:])
    quotient=Registers[rega]//Registers[regb]
    remainder=Registers[rega]%Registers[regb]
    Registers[0]=quotient
    Registers[1]=remainder
    checkOverflow()

def inv(instruction):
    to_store = instruction[0:3]
    regb = ConvertToDecimal(instruction[3:])
    invert=2**8-1-Registers[regb]
    Registers[ConvertToDecimal(
        to_store)] = invert

def cmp(instruction):
    global flag
    a = Registers[ConvertToDecimal(instruction[0:3])]
    b = Registers[ConvertToDecimal(instruction[3:])]
    if (a<b):
        flag=4
    elif (a>b):
        flag=2
    else:
        flag=1

def execution_engine(instruction_bin):
    opcode = instruction_bin[:5]
    op = OpCode[opcode]
    if (op == "add"):
        rest_bin = instruction_bin[7:]
        add(rest_bin)
        outputOneLine()
    elif (op == "sub"):
        rest_bin = instruction_bin[7:]
        sub(rest_bin)
        outputOneLine()
    elif (op == "mul"):
        rest_bin = instruction_bin[7:]
        mul(rest_bin)
        outputOneLine()
    elif (op == "xor"):
        rest_bin = instruction_bin[7:]
        xor(rest_bin)
        outputOneLine()
    elif (op == "or"):
        rest_bin = instruction_bin[7:]
        BITor(rest_bin)
        outputOneLine()
    elif (op == "and"):
        rest_bin = instruction_bin[7:]
        BITand(rest_bin)
        outputOneLine()
    elif (op == "rs"):
        rest_bin = instruction_bin[5:]
        rs(rest_bin)
        outputOneLine()
    elif (op == "ls"):
        rest_bin = instruction_bin[5:]
        ls(rest_bin)
        outputOneLine()
    elif (op == "movI"):
        rest_bin = instruction_bin[5:]
        movI(rest_bin)
        outputOneLine()
    elif (op == "movR"):
        rest_bin = instruction_bin[10:]
        movR(rest_bin)
        outputOneLine()
    elif (op == "movR"):
        rest_bin = instruction_bin[10:]
        movR(rest_bin)
        outputOneLine()
    elif (op == "div"):
        rest_bin = instruction_bin[10:]
        div(rest_bin)
        outputOneLine()
    elif (op == "inv"):
        rest_bin = instruction_bin[10:]
        inv(rest_bin)
        outputOneLine()
    elif (op == "cmp"):
        rest_bin = instruction_bin[10:]
        cmp(rest_bin)
        outputOneLine()

if (__name__ == "__main__"):
    initializeMem()
    while(n != 1001100000000000):
        n = input()
        Instructions.append(n)
        
        Execute = memory(ConvertToBinary8(pc))
