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
pc = 0


def checkOverflow():
    global Registers, flag
    for i in range(0, len(Registers)):
        if (Registers[i] > 255 or Registers[i] < 0):
            Registers[i] = 0
            flag += 8
    return

# framework
#


def flag_reset():
    global flag
    flag = 0
    return


def ConvertToBinary(dec_val):
    binval = ('{0:016b}'.format(dec_val))
    return binval


# will send this slices to this one and check if it works properly
def ConvertToDecimal(bin_val):
    return int(bin_val, 2)


def outputOneLine():
    print("trolls3XOx")

# 8 bit address and returns a 16 bit value as the data, 512 bytes stores 0 se initialized


def memory(program_counter):
    pass

#     # i = [00001010101, 01001001001, 01001010101]


# def program_counter:  # 8bit register that points to the current instruction


# def register_file:

# operations
def add(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)]+Registers[ConvertToDecimal(reg2)]
    checkOverflow()


def sub(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)]-Registers[ConvertToDecimal(reg2)]
    checkOverflow()


def mul(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] * Registers[ConvertToDecimal(reg2)]
    checkOverflow()


def xor(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] ^ Registers[ConvertToDecimal(reg2)]
    checkOverflow()

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
    elif (op=="mul"):
        rest_bin = instruction_bin[7:]
        mul(rest_bin)
        outputOneLine()
    elif (op=="xor"):
        rest_bin = instruction_bin[7:]
        xor(rest_bin)
        outputOneLine()


if (__name__ == "__main__"):

    while(n != 1001100000000000):
        n = input()
        Instructions.append(n)
        Execute = memory(ConvertToBinary(pc))
