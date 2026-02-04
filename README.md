# IAS Architecture Design

This repository contains a Python-based implementation of the IAS (Institute for Advanced Study) computer architecture. The project demonstrates the conversion of assembly language instructions into machine code and their execution using a simulated IAS instruction cycle.

The implementation is intended for academic and educational purposes to support the study of computer organization and architecture.

---

## Repository Structure

.
├── assembler.py        Assembler for generating machine code  
├── ias.py              IAS architecture simulator  
├── assembly.txt        Input assembly program  
├── binary.txt          Generated machine code  
└── README.md           Documentation  

---

## Project Overview

The project consists of two components:

1. **Assembler**  
   Reads instructions from `assembly.txt` and converts them into binary machine code stored in `binary.txt`.

2. **IAS Simulator**  
   Loads the binary instructions and executes them by simulating the IAS fetch–decode–execute cycle.

---

## Requirements

- Python 3.x

---

## Execution Procedure

### Step 1: Clone the Repository

git clone https://github.com/ArushJain-697/IAS-architecture-design.git  
cd IAS-architecture-design

---

### Step 2: Run the Assembler

python3 assembler.py

This generates the binary machine code in `binary.txt`.

---

### Step 3: Run the Simulator

python3 ias.py

The simulator executes the program and displays the execution results.

---

## Notes

- All files must be located in the same directory.
- This is a simplified IAS architecture model intended for instructional use.
