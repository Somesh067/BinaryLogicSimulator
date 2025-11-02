# BinaryLogicSimulator
Intelligent Binary Logic Simulator

Welcome to the Intelligent Binary Logic Simulator, an educational tool designed to bridge the gap between abstract digital logic theory and practical, observable computation.

This project demonstrates how complex arithmetic operations (like addition, subtraction, multiplication, and division) are performed using only the most fundamental logic gates (AND, OR, NOT, XOR).

It exists in two forms:

A modular Python/Tkinter desktop application.

A modern, single-file HTML/JavaScript web application.

Core Features

Gate-Level Simulation: Interactively simulate fundamental logic gates (AND, OR, NOT, XOR, etc.) with SVG diagrams and a live truth table.

Gate-Level Arithmetic: Perform 8-bit binary arithmetic (ADD, SUB, MUL, DIV) and see the step-by-step trace of how the logic gates compute the result.

ALU Simulation: A mini-ALU (Arithmetic Logic Unit) demonstrates how operations are selected and how status flags (Zero, Carry, Overflow, Sign) are set.

Logic Expression Designer: Write your own Boolean expressions (e.g., (A AND B) OR NOT C), generate full truth tables, and run a step-by-step simulation of the expression's evaluation.

Interactive I/O:

Web App: Features a dynamic virtual keypad, multiple base inputs (Binary, Decimal, Octal, Hex), and responsive design for all devices.

Python App: A classic desktop GUI built with Tkinter.

Project Documentation

For a complete understanding of the project, please see the following documents:

PROJECT_SUMMARY.md: A high-level overview of the project's goals and features.

QUICKSTART.md: Get up and running! Instructions for launching both the Web and Python versions.

TECHNICAL_DOCUMENTATION.md: A deep dive into the project architecture, file structure, and the algorithms used (e.g., Restoring Division, Shunting-Yard).

CIRCUIT_DIAGRAMS.md: Visual (ASCII) diagrams explaining how circuits like the Full Adder and 2's Complement Subtractor are built from basic gates.

Technology Stacks

1. Web Application (Recommended)

HTML5: Semantic structure.

Tailwind CSS: Modern, responsive styling.

JavaScript (ES6+): All logic (gates, arithmetic, ALU) was ported from Python to plain JavaScript classes. No frameworks are used.

2. Python Desktop Application

Python 3.6+: Core logic and algorithms.

Tkinter: Built-in Python library for the graphical user interface (GUI).

Modular Design: Logic is separated into modules (logic_gates, binary_arithmetic, alu_simulator, etc.).

Educational Goals

This simulator was built to answer the question: "How does a computer actually compute?" By forcing all operations to be built from the ground up, users can:

Visualize the connection between a single AND gate and a complex DIVIDE operation.

Understand how an ALU processes instructions and sets status flags.

Learn how Boolean algebra is parsed and evaluated.

Appreciate the levels of abstraction that make modern computing possible.
