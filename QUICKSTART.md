Quickstart Guide

This project is available in two versions. The Web Application is recommended for general use, as it requires no setup.

Version 1: Web Application (Recommended)

This version runs on any modern browser (Chrome, Firefox, Safari, Edge) on desktop or mobile.

How to Run

Download the logic_simulator.html file.

Open the file in your web browser.

That's it! The entire simulator is self-contained in that single file.

Version 2: Python Desktop Application

This version runs as a native desktop application on Windows, macOS, and Linux.

Prerequisites

Python 3.6 or newer.

Tkinter: This is included with most standard Python installations. If it's not, you may need to install it:

Linux (Debian/Ubuntu): sudo apt-get install python3-tk

Linux (Fedora): sudo dnf install python3-tkinter

File Structure

Ensure your files are arranged in the following structure:

project_root/
├── src/
│   ├── gui.py                 # The main application file
│   ├── logic_gates.py
│   ├── binary_analyzer.py
│   ├── binary_arithmetic.py
│   ├── logic_designer.py
│   └── alu_simulator.py
└── ... (other docs)


How to Run

Open your terminal or command prompt.

Navigate to the project_root directory.

Run the gui.py file from within the src folder:

python src/gui.py


The application window should appear.

How to Use the Simulator

The interface for both applications is divided into four main tabs:

1. Logic Gates Tab (Web App Only)

What it does: Simulates a single logic gate (AND, OR, NOT, etc.).

How to use:

Select a gate from the dropdown menu.

Click the Input A and Input B switches to toggle them between 0 and 1.

Observe the SVG diagram, output LED, and live truth table update instantly.

2. Arithmetic Operations Tab

What it does: Performs 8-bit arithmetic (ADD, SUB, MUL, DIV) and shows the step-by-step internal logic.

How to use:

Select the input base (Binary, Decimal, Octal, or Hex) for Operand A and Operand B.

Enter values using your physical keyboard or the virtual keypad.

Click one of the operation buttons (e.g., ADD).

The binary LED displays will show the inputs and the result.

The Execution Trace log will fill with a detailed, step-by-step account of the gate-level operations.

3. Logic Designer Tab

What it does: Lets you create, test, and simulate your own Boolean expressions.

How to use:

Type a Boolean expression in the input field (e.g., (A AND B) OR NOT C).

Click "Generate Truth Table" to see all possible outcomes.

Click "Simulate Step-by-Step" to evaluate the expression with specific inputs (e.g., A=1, B=0, C=1) and see the evaluation trace.

4. ALU Simulator Tab

What it does: Simulates a simple Arithmetic Logic Unit.

How to use:

Enter Operand A and Operand B (just like the Arithmetic tab).

Select an operation (e.g., ADD, SHL, ROR) from the dropdown.

Click "Execute".

The ALU will perform the operation, and the Status Flags (Zero, Carry, Overflow, Sign, Parity) will update based on the result.

The ALU Execution Log will show the trace for the selected operation.
