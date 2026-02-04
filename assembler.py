import sys
def main():
    opcodes = {
        'HALT': '11111111',
        'NOP': '10000000',
        'LOAD': '00000001',
        'LOAD-': '00000010',
        'LOAD|': '00000011',
        'LOAD-|': '00000100',
        'LOADMQ': '00001010',
        'LOADMQ_M': '00001001',
        'STOR': '00100001',
        'ADD': '00000101',
        'SUB': '00000110',
        'ADD|': '00000111',
        'SUB|': '00001000',
        'MUL': '00001011',
        'DIV': '00001100',
        'LSH': '00010100',
        'RSH': '00010101',
        'STOR_L': '00010010',
        'STOR_R': '00010011'}
    jump_ops = {
        'JUMP': {'left': '00001101', 'right': '00001110'},
        'JUMP+': {'left': '00001111', 'right': '00010000'},
        'JUMP++': {'left': '00011000', 'right': '00011001'}}
    input_file = "assembly.txt"
    output_file = "binary.txt"
    memory = []
    for i in range(1024):
        memory.append("0" * 40)
    try:
        with open(input_file, 'r') as f:
            raw_lines = f.readlines()
    except:
        print("Error: cant open file")
        return
    lines = []
    for line in raw_lines:
        line = line.split('//')[0].strip()
        if len(line) > 0:
            lines.append(line)
    pc = 0
    is_left = True
    temp_pair = ["", ""]
    for line in lines:
        if line.startswith('.data'):
            parts = line.split()
            addr = int(parts[1])
            val = int(parts[2])      
            if val < 0:
                val = (1 << 40) + val
            
            memory[addr] = format(val, '040b')
            continue
        parts = line.split()
        op_name = parts[0]
        arg = ""
        if len(parts) > 1:
            arg = parts[1]
        addr_val = 0
        is_right_target = False

        if "M(" in arg:
            clean = arg.replace("M(", "").replace(")", "")
            if "," in clean:
                addr_str, range_str = clean.split(",")
                addr_val = int(addr_str)
                if "20:39" in range_str:
                    is_right_target = True
            else:
                addr_val = int(clean)

        bin_op = "00000000"
        if op_name in opcodes:
            bin_op = opcodes[op_name]
        elif op_name in jump_ops:
            if is_right_target:
                bin_op = jump_ops[op_name]['right']
            else:
                bin_op = jump_ops[op_name]['left']
        else:
            print("Unknown opcode:", op_name)

        bin_addr = format(addr_val, '012b')
        instr = bin_op + bin_addr

        if is_left:
            temp_pair[0] = instr
            is_left = False
        else:
            temp_pair[1] = instr
            full_word = temp_pair[0] + temp_pair[1]
            memory[pc] = full_word
            pc += 1
            is_left = True
            temp_pair = ["", ""]
    if not is_left:
        full_word = temp_pair[0] + "00000000000000000000"
        memory[pc] = full_word

    with open(output_file, 'w') as out:
        for word in memory:
            out.write(word + "\n")   
    print("binary file is updated now bhaiya")
main()