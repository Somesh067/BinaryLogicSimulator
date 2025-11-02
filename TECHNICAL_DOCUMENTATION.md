Technical Documentation

1. Project Overview & Architecture

The Intelligent Binary Logic Simulator is a modular application designed for educational purity. The core architectural philosophy is "build from the ground up." No high-level arithmetic or logic operators (like +, *, eval()) are used for the core computations. Every operation is built from the foundational LogicGates class.

The architecture follows a clear hierarchy of abstraction:

Level 0: Logic Gates (logic_gates.py)

Implements AND, OR, NOT, XOR, etc., as pure functions.

Level 1: Combinational Circuits (logic_gates.py)

Combines gates to create HalfAdder and FullAdder.

Level 2: Arithmetic Units (binary_arithmetic.py)

Chains FullAdders to create a RippleCarryAdder.

Uses the adder to create TwosComplement and Subtract units.

Implements sequential algorithms (Multiply, Divide) that use the adder/subtractor as components.

Level 3: ALU & Control (alu_simulator.py)

The ALU class wraps all arithmetic/logic units.

The ControlUnit class decodes an "opcode" to select which ALU function to execute.

ALUFlags calculates status flags (Zero, Sign, Carry, Overflow) based on the result.

Level 4: Application Layer (gui.py / logic_simulator.html)

Provides a user interface to interact with the underlying logic, visualize the results, and display the step-by-step execution traces.

2. Core Modules (Python Implementation)

This details the original Python application's structure.

src/logic_gates.py

Class: LogicGates (static methods)

Class: CombinationalCircuits (static methods)

Purpose: The foundation of the entire project. All other modules depend on this file.

src/binary_analyzer.py

Class: BinaryAnalyzer (static methods)

Purpose: A utility module for binary-decimal conversion, parity checking, and formatting binary strings for logs. It does not perform arithmetic.

src/binary_arithmetic.py

Class: BinaryArithmetic

Purpose: The core "engine" of the simulator. It implements the arithmetic algorithms and generates detailed execution traces.

Key Feature: The _add_step() method allows the class to log its internal state at every step of an algorithm, providing the "Execution Trace" for the UI.

src/logic_designer.py

Class: LogicExpressionParser

Algorithm: Uses the Shunting-Yard Algorithm to convert the user's infix expression (e.g., A AND B) into a postfix (Reverse Polish Notation) list (e.g., ['A', 'B', 'AND']).

Algorithm: Uses a simple stack-based evaluator to compute the result from the postfix list.

Class: CircuitSimulator

Purpose: Wraps the parser to provide a step-by-step trace of the stack evaluation.

src/alu_simulator.py

Class: ALUFlags

Purpose: A stateful class to hold and calculate the Z/C/O/S/P flags.

Class: ALU

Purpose: A wrapper that contains an instance of BinaryArithmetic. It selects the correct operation based on an opcode and updates the ALUFlags instance.

Class: ControlUnit

Purpose: Provides a high-level decode_and_execute method that mimics a CPU's control unit, directing the ALU.

src/gui.py

Framework: tkinter (Python standard library)

Purpose: The main application entry point. It creates the tabbed notebook interface, wires all the buttons to the underlying logic classes, and formats the trace data for display in the scrolledtext widgets.

3. Web Application (JavaScript Port)

The web application (logic_simulator.html) is a direct, single-file port of the entire Python project.

Architecture: A single HTML file containing three main sections:

<head>: Includes <style> (Tailwind CSS) for all styling.

<body>: Contains the HTML for the tabbed interface, keypads, and displays.

<script type="module">: Contains all the logic, ported from Python to JavaScript.

Logic Porting:

All Python classes (LogicGates, BinaryArithmetic, ALU, etc.) were converted one-to-one into JavaScript ES6 classes.

Python's staticmethods became static methods in JavaScript.

Python's lists used as binary numbers ([0, 1, 0, 1]) were converted directly to JavaScript Arrays ([0, 1, 0, 1]).

The execution trace generation (_add_step) and formatting (_format_trace) logic was preserved identically.

Key Enhancements (Web-only):

Dynamic I/O: The virtual keypad and input fields are context-aware. The updateKeypad function enables/disables keys based on the selected base (Binary, Decimal, Octal, Hex).

Input Validation: BinaryAnalyzer.isValidChar is used to prevent invalid characters from being entered via physical or virtual keyboard.

SVG Gate Simulation: The "Logic Gates" tab uses inline SVG elements. JavaScript directly manipulates the style and data-value attributes of the SVG paths and wires to create the live visualization.

4. Core Algorithm Explanations

Addition: Ripple Carry Adder

See: CIRCUIT_DIAGRAMS.md

Implementation: A simple for loop (from i = 0 to bit_width - 1) that iterates through the bits. Each iteration calls the CombinationalCircuits.full_adder function, passing the carry_out of one step as the carry_in to the next.

Subtraction: 2's Complement

See: CIRCUIT_DIAGRAMS.md

Implementation: A - B is implemented as A + (NOT B) + 1.

twos_complement(B) is called, which first inverts all bits of B.

It then uses the ripple_carry_adder to add 1 to the inverted bits.

subtract() then calls ripple_carry_adder(A, twos_complement_of_B).

The final carry_out of this addition is inverted to produce the borrow flag.

Multiplication: Shift-and-Add

Algorithm: This mimics binary long multiplication. A 16-bit product is initialized to zero.

Implementation:

Loop i from 0 to 7 (for each bit of the multiplier B).

Check B[i] (the i-th bit of the multiplier).

If B[i] == 1: Add the multiplicand (A) to the product.

If B[i] == 0: Add nothing.

Shift the multiplicand one position to the left (preparing it for the next bit).

Repeat.

The final 16-bit product is returned.

Division: Restoring Division

Algorithm: This is a sequential algorithm that mimics binary long division. It uses a Quotient register Q (initially the dividend) and a Remainder register A (initially zero).

Implementation:

Check for divide-by-zero.

Loop i from 0 to 7 (one for each bit).

Shift: Shift the combined (A, Q) register one position to the left.

Subtract: Calculate A = A - M (where M is the divisor).

Check Sign: Look at the most-significant-bit (MSB) of A.

If A is negative (MSB == 1): The subtraction was unsuccessful.

Set the new LSB of Q to 0.

Restore: Add M back to A (i.e., A = A + M) to undo the subtraction.

If A is positive (MSB == 0): The subtraction was successful.

Set the new LSB of Q to 1.

Repeat.

After 8 loops, Q holds the quotient and A holds the remainder.
