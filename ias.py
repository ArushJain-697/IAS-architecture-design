import sys
import os
ac = 0
mq = 0
mbr = 0
ir = 0
mar = 0
pc = 0
ibr = 0
has_right = False
halt = False
def read_mem(addr):
    try:
        with open("binary.txt", "r") as f:
            lines = f.readlines()
            if addr < len(lines):
                return lines[addr].strip()
            else:
                return "0" * 40
    except:
        print("Error: Could not read binary.txt")
        sys.exit(1)

def write_mem(addr, val):
    try:

        with open("binary.txt", "r") as f:
            lines = f.readlines()
        while len(lines) <= addr:
            lines.append("0" * 40 + "\n")
        lines[addr] = val + "\n"
        with open("binary.txt", "w") as f:
            f.writelines(lines)
            f.flush()      
            os.fsync(f.fileno())             
    except Exception as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)
        
def to_int(binary_str):
    val = int(binary_str, 2)
    if binary_str[0] == '1':
        val -= (1 << 40)
    return val

def to_bin(val, bits):
    val = int(val) & ((1 << bits) - 1)
    fmt = '0' + str(bits) + 'b'
    return format(val, fmt)

def print_registers():
    print("PC  : " + to_bin(pc, 12))
    print("AC  : " + to_bin(ac, 40))
    print("MQ  : " + to_bin(mq, 40))
    print("IR  : " + to_bin(ir >> 12, 8))
    print("MBR : " + to_bin(mbr, 40))
    print("MAR : " + to_bin(mar, 12))
    print("-" * 40)

def fetch():
    global ir, ibr, pc, mar, mbr, has_right
    if has_right:
        ir = ibr
        has_right = False
        pc += 1
    else:
        mar = pc
        val_str = read_mem(mar)
        mbr = int(val_str, 2)
        ir = (mbr >> 20) & 0xFFFFF
        ibr = mbr & 0xFFFFF
        has_right = True

def execute():
    global ac, mq, pc, mar, mbr, ibr, has_right, halt
    op = (ir >> 12) & 0xFF
    addr = ir & 0xFFF
    mar = addr
    if op == 1:
        val = read_mem(addr)
        ac = to_int(val)
    elif op == 2:
        val = read_mem(addr)
        ac = -to_int(val)
    elif op == 3:
        val = read_mem(addr)
        ac = abs(to_int(val))
    elif op == 4:
        val = read_mem(addr)
        ac = -abs(to_int(val))
    elif op == 5:
        val = read_mem(addr)
        ac += to_int(val)
    elif op == 6:
        val = read_mem(addr)
        ac -= to_int(val)
    elif op == 7:
        val = read_mem(addr)
        ac += abs(to_int(val))
    elif op == 8:
        val = read_mem(addr)
        ac -= abs(to_int(val))
    elif op == 9:
        val = read_mem(addr)
        mq = to_int(val)
    elif op == 10:
        ac = mq
    elif op == 11:
        val = to_int(read_mem(addr))
        ac = ac * val
        mq = ac
    elif op == 12:
        val = to_int(read_mem(addr))
        if val != 0:
            mq = ac // val
            ac = ac % val
    elif op == 13:
        pc = addr
        has_right = False
    elif op == 14:
        pc = addr
        mar = pc
        val_str = read_mem(mar)
        mbr = int(val_str, 2)
        ibr = mbr & 0xFFFFF
        has_right = True
    elif op == 15:
        if ac >= 0:
            pc = addr
            has_right = False
    elif op == 16:
        if ac >= 0:
            pc = addr
            mar = pc
            val_str = read_mem(mar)
            mbr = int(val_str, 2)
            ibr = mbr & 0xFFFFF
            has_right = True
    elif op == 18: 
        old_val = read_mem(addr)
        new_addr_bin = to_bin(ac & 0xFFF, 12)
        new_val = old_val[:8] + new_addr_bin + old_val[20:]
        write_mem(addr, new_val)
    elif op == 19: 
        old_val = read_mem(addr)
        new_addr_bin = to_bin(ac & 0xFFF, 12)
        new_val = old_val[:28] + new_addr_bin
        write_mem(addr, new_val)
    elif op == 20:
        ac = ac << 1
    elif op == 21:
        ac = ac >> 1
    elif op == 24:
        if ac > 0:
            pc = addr
            has_right = False
    elif op == 25:
        if ac > 0:
            pc = addr
            mar = pc
            val_str = read_mem(mar)
            mbr = int(val_str, 2)
            ibr = mbr & 0xFFFFF
            has_right = True
    elif op == 33: 
        bin_str = to_bin(ac, 40)
        write_mem(addr, bin_str)
        mbr = ac
    elif op == 255:
        halt = True

def run():
    cycles = 0
    print("Simulating IAS Machine...")
    while not halt and cycles < 2000:
        fetch()
        print("\n[Cycle " + str(cycles) + ": FETCH Completed]")
        print_registers()
        input("Press Enter to Execute...")
        execute()
        print("\n[Cycle " + str(cycles) + ": EXECUTE Completed]")
        print_registers()
        if not halt:
            input("press Enter for next cycle")    
        cycles += 1
    print("       FINAL PROCESSOR STATE")
    print_registers()
run()
