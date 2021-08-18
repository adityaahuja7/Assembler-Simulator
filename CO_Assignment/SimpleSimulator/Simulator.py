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

Instructions = []
pc = 0

#framework 
#
def ConvertToBinary(dec_val):
    binval = ('{0:016b}'.format(dec_val))
    return binval


# 8 bit address and returns a 16 bit value as the data, 512 bytes stores 0 se initialized
def memory(program_counter):


def program_counter:  # 8bit register that points to the current instruction


def register_file:


def execution_engine:


if __name__ == "__main__":
    while(n != 1001100000000000):
        n = input()
        Instructions.append(n)
    Execute = 

# poggi code
# <program counter> <registers from 0 to 6 and flags>
# memory dump 256 lines, 16 bit values
#
