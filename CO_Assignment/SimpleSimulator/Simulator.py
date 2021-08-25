import matplotlib.pyplot as plt

# Registers and flags
#code
flag = 0
Registers = [0, 0, 0, 0, 0, 0, 0]

# mapping of program counter and memory address
pc_and_cycle = []

halted = False

OpCode = {
    "00000": "add", "00001": "sub", "00010": "movI", "00011": "movR", "00100": "ld",
    "00101": "st", "00110": "mul", "00111": "div", "01000": "rs", "01001": "ls",
    "01010": "xor", "01011": "or", "01100": "and", "01101": "inv", "01110": "cmp", "01111": "jmp",
    "10000": "jlt", "10001": "jgt", "10010": "je", "10011": "halt"
}

# 8 bits required to represent memory address, one address contains a 16 bit binary
Memory_Heap = []
Binary_input = []
pc = 0
cycle = 1


def checkOverflow(ind):
    global Registers, flag
    if (Registers[ind] > 2**16-1 or Registers[ind] < 0):
        flag = 8
        if (Registers[ind] > 2**16-1):
            Registers[ind] = int(ConvertToBinary16(Registers[ind]), 2)
        else:
            Registers[ind] = 0
    return


def flag_reset():  # resets flag do use this wherever necessary
    global flag
    flag = 0
    return


def ConvertToBinary16(dec_val):
    if (dec_val > 2**16-1):
        bin_rep = str(bin(dec_val))
        bin_rep = bin_rep[2::]
        l = len(bin_rep)
        bin_rep = bin_rep[l-16:l:]
        binval = int(bin_rep, 2)
        binval = ('{0:016b}'.format(binval))
    else:
        binval = ('{0:016b}'.format(dec_val))
    return binval


def ConvertToBinary8(dec_val):
    binval = ('{0:08b}'.format(dec_val))
    return binval


def ConvertToDecimal(bin_val):
    return int(bin_val, 2)


def outputOneLine():
    global pc, cycle, pc_and_cycle
    print(
        ConvertToBinary8(pc),
        ConvertToBinary16(Registers[0]),
        ConvertToBinary16(Registers[1]),
        ConvertToBinary16(Registers[2]),
        ConvertToBinary16(Registers[3]),
        ConvertToBinary16(Registers[4]),
        ConvertToBinary16(Registers[5]),
        ConvertToBinary16(Registers[6]),
        ConvertToBinary16(flag),
        sep=" "
    )
    pc_and_cycle.append((pc, cycle))
    cycle += 1


# 8 bit address and returns a 16 bit value as the data, 512 bytes stores 0 se initialized


def initializeMem():
    for j in range(256):
        Memory_Heap.append("0000000000000000")
    return


def UpdatePC():
    global pc
    pc += 1


# def program_counter:  # 8bit register that points to the current instruction


# operations
def add(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] + Registers[ConvertToDecimal(reg2)]
    checkOverflow(ConvertToDecimal(to_store))
    return


def sub(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] - Registers[ConvertToDecimal(reg2)]
    checkOverflow(ConvertToDecimal(to_store))
    return


def mul(instruction):
    to_store = instruction[0:3]
    reg1 = instruction[3:6]
    reg2 = instruction[6:9]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] * Registers[ConvertToDecimal(reg2)]
    checkOverflow(ConvertToDecimal(to_store))
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
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        to_store)] // (2 ** value)
    return


def ls(instruction):
    to_store = instruction[0:3]
    value = ConvertToDecimal(instruction[3:])
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        to_store)] * (2 ** value)
    if (Registers[ConvertToDecimal(to_store)] > 2**16-1):
        Registers[ConvertToDecimal(to_store)] = int(
            ConvertToBinary16(to_store), 2)
    return


def movI(instruction):
    to_store = instruction[0:3]
    value = ConvertToDecimal(instruction[3:])
    Registers[ConvertToDecimal(to_store)] = value
    return


def movR(instruction):
    global flag
    to_store = instruction[0:3]
    reg_aux = ConvertToDecimal(instruction[3:])
    if (reg_aux == 7):
        Registers[ConvertToDecimal(to_store)] = flag
    else:
        Registers[ConvertToDecimal(to_store)] = Registers[reg_aux]
    return


def div(instruction):
    rega = ConvertToDecimal(instruction[0:3])
    regb = ConvertToDecimal(instruction[3:])
    quotient = Registers[rega] // Registers[regb]
    remainder = Registers[rega] % Registers[regb]
    Registers[0] = quotient
    Registers[1] = remainder
    return


def inv(instruction):
    to_store = instruction[0:3]
    regb = ConvertToDecimal(instruction[3:])
    invert = 2 ** 16 - 1 - Registers[regb]
    Registers[ConvertToDecimal(to_store)] = invert
    return


def compare(instruction):
    global flag
    a = Registers[ConvertToDecimal(instruction[0:3])]
    b = Registers[ConvertToDecimal(instruction[3:])]
    if (a < b):
        flag = 4
    elif (a > b):
        flag = 2
    else:
        flag = 1
    return


def ld(instruction):
    to_store = ConvertToDecimal(instruction[:3])
    address = ConvertToDecimal(instruction[3:])
    Registers[to_store] = ConvertToDecimal(
        ConvertToBinary16(Memory_Heap[address]))
    return


def st(instruction):
    global Memory_Heap
    source_reg = ConvertToDecimal(instruction[:3])
    address = ConvertToDecimal(instruction[3:])
    Memory_Heap[address] = ConvertToBinary16(Registers[source_reg])
    return


def jmp(instruction):
    global pc
    mem_add = ConvertToDecimal(instruction)
    pc = mem_add
    return


def jlt(instruction):
    global pc, flag
    mem_add = ConvertToDecimal(instruction)
    if (flag == 4):
        pc = mem_add
    else:
        pc += 1
    return


def jgt(instruction):
    global pc, flag
    mem_add = ConvertToDecimal(instruction)
    if (flag == 2):
        pc = mem_add
    else:
        pc += 1
    return


def je(instruction):
    global pc, flag
    mem_add = ConvertToDecimal(instruction)
    if (flag == 1):
        pc = mem_add
    else:
        pc += 1
    return


def execution_engine():
    global flag, cycle, pc, Memory_Heap, halted
    instruction_bin = Memory_Heap[pc]
    opcode = instruction_bin[:5]
    op = OpCode[opcode]

    if (op!="movR" and op != "jlt" and op != "jgt" and op != "je"): #implementation based if condition
        flag_reset()
        
    if (op == "add"):
        rest_bin = instruction_bin[7:]
        add(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "sub"):
        rest_bin = instruction_bin[7:]
        sub(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "mul"):
        rest_bin = instruction_bin[7:]
        mul(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "xor"):
        rest_bin = instruction_bin[7:]
        xor(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "or"):
        rest_bin = instruction_bin[7:]
        BITor(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "and"):
        rest_bin = instruction_bin[7:]
        BITand(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "rs"):
        rest_bin = instruction_bin[5:]
        rs(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "ls"):
        rest_bin = instruction_bin[5:]
        ls(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "movI"):
        rest_bin = instruction_bin[5:]
        movI(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "movR"):
        rest_bin = instruction_bin[10:]
        movR(rest_bin)
        flag_reset()
        outputOneLine()
        UpdatePC()
    elif (op == "div"):
        rest_bin = instruction_bin[10:]
        div(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "inv"):
        rest_bin = instruction_bin[10:]
        inv(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "cmp"):
        rest_bin = instruction_bin[10:]
        compare(rest_bin)
        outputOneLine() 
        UpdatePC()
    elif (op == "ld"):
        rest_bin = instruction_bin[5:]
        ld(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "st"):
        rest_bin = instruction_bin[5:]
        st(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "jmp"):
        rest_bin = instruction_bin[8:]
        outputOneLine()
        jmp(rest_bin)
    elif (op == "jlt"):
        rest_bin = instruction_bin[8:]
        temp=flag
        flag=0
        outputOneLine()
        flag=temp
        jlt(rest_bin)
        flag_reset()
    elif (op == "jgt"):
        rest_bin = instruction_bin[8:]
        temp=flag
        flag=0
        outputOneLine()
        flag=temp
        jgt(rest_bin)
        flag_reset()
    elif (op == "je"):
        rest_bin = instruction_bin[8:]
        #next 4 lines only for printing
        temp = flag
        flag = 0
        outputOneLine()
        flag = temp
        je(rest_bin)
        flag_reset()
    else:
        halted = True
        outputOneLine()


def TakeInput():
    global pc, Binary_input, halted
    initializeMem()
    bin_in = ""
    address = 0

    while (bin_in != "1001100000000000"):
        bin_in = input()
        Memory_Heap[address] = bin_in[::]
        address += 1

    while (not halted):
        execution_engine()


# # bonus part
def scatterPlot():
    global pc_and_cycle  # (pc,cycle)
    x_axis = []
    y_axis = []
    for i in pc_and_cycle:
        x_axis.append(i[1])
        y_axis.append(i[0])
    plt.scatter(x_axis, y_axis, c="blue")
    plt.xlabel("Cycles")
    plt.ylabel("Program_Counter(Mem_Address)")
    plt.show()


if __name__ == "__main__":
    TakeInput()
    for i in Memory_Heap:
        print(i)
    scatterPlot()
