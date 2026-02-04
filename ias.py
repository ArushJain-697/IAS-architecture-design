import sys
mem = ["0" * 40] * 1024
ac = 0
mq = 0
mbr = 0
ir = 0
mar = 0
pc = 0
ibr = 0
has_right = False
halt = False
def to_int(binary_str):
    val = int(binary_str, 2)
    if binary_str[0] == '1':
        val -= (1 << 40)
    return val
def to_bin(val, bits):
    val = int(val) & ((1 << bits) - 1)
    fmt = '0' + str(bits) + 'b'
    return format(val, fmt)
def load_file(filename):
    global mem
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if i < 1024:
                    mem[i] = lines[i].strip()
    except:
        print("there is an error reading file")
        sys.exit(1)

def fetch():
    global ir, ibr, pc, mar, mbr, has_right
    if has_right:
        ir = ibr
        has_right = False
        pc += 1
    else:
        mar = pc
        mbr = int(mem[mar], 2)
        ir = (mbr >> 20) & 0xFFFFF
        ibr = mbr & 0xFFFFF
        has_right = True

def execute():
    global ac, mq, mem, pc, mar, mbr, ibr, has_right, halt
    op = (ir >> 12) & 0xFF
    addr = ir & 0xFFF
    mar = addr

    if op == 1:
        ac = to_int(mem[addr])
    elif op == 2:
        ac = -to_int(mem[addr])
    elif op == 3:
        ac = abs(to_int(mem[addr]))
    elif op == 4:
        ac = -abs(to_int(mem[addr]))
    elif op == 5:
        ac += to_int(mem[addr])
    elif op == 6:
        ac -= to_int(mem[addr])
    elif op == 7:
        ac += abs(to_int(mem[addr]))
    elif op == 8:
        ac -= abs(to_int(mem[addr]))
    elif op == 9:
        mq = to_int(mem[addr])
    elif op == 10:
        ac = mq
    elif op == 11:
        val = to_int(mem[addr])
        ac = ac * val
        mq = ac
    elif op == 12:
        val = to_int(mem[addr])
        if val != 0:
            mq = ac // val
            ac = ac % val
    elif op == 13:
        pc = addr
        has_right = False
    elif op == 14:
        pc = addr
        mar = pc
        mbr = int(mem[mar], 2)
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
            mbr = int(mem[mar], 2)
            ibr = mbr & 0xFFFFF
            has_right = True
    elif op == 18:
        old = mem[addr]
        new_addr = to_bin(ac & 0xFFF, 12)
        mem[addr] = old[:8] + new_addr + old[20:]
    elif op == 19:
        old = mem[addr]
        new_addr = to_bin(ac & 0xFFF, 12)
        mem[addr] = old[:28] + new_addr
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
            mbr = int(mem[mar], 2)
            ibr = mbr & 0xFFFFF
            has_right = True
    elif op == 33:
        mem[addr] = to_bin(ac, 40)
        mbr = ac
    elif op == 255:
        halt = True
def run():
    cycles = 0
    while not halt and cycles < 2000:
        fetch()
        execute()
        cycles += 1
    print("PC  : " + to_bin(pc, 12))
    print("AC  : " + to_bin(ac, 40))
    print("MQ  : " + to_bin(mq, 40))
    print("IR  : " + to_bin(ir >> 12, 8))
    print("MBR : " + to_bin(mbr, 40))
    print("MAR : " + to_bin(mar, 12))
load_file("binary.txt")
run()