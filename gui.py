"""
Intelligent Binary Logic Simulator - Main GUI
==============================================
Interactive graphical interface for visualizing digital logic operations
and ALU simulation with step-by-step execution.

Author: Digital Logic Educational Project
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic_gates import LogicGates, CombinationalCircuits
from binary_arithmetic import BinaryArithmetic
from binary_analyzer import BinaryAnalyzer
from alu_simulator import ALU, ControlUnit, ALUFlags
from logic_designer import LogicExpressionParser, CircuitSimulator


class BinaryLED(tk.Canvas):
    """
    LED-style binary digit display widget.
    """

    def __init__(self, parent, **kwargs):
        """Initialize LED display."""
        super().__init__(parent, width=30, height=30,
                         highlightthickness=1, **kwargs)
        self.value = 0
        self.draw()

    def set_value(self, value: int):
        """Set LED value (0 or 1)."""
        self.value = value
        self.draw()

    def draw(self):
        """Draw LED circle."""
        self.delete("all")
        color = "#00FF00" if self.value == 1 else "#404040"
        border = "#00AA00" if self.value == 1 else "#202020"

        self.create_oval(5, 5, 25, 25, fill=color, outline=border, width=2)

        # Draw value
        text_color = "#000000" if self.value == 1 else "#808080"
        self.create_text(15, 15, text=str(self.value),
                         fill=text_color, font=("Arial", 10, "bold"))


class BinaryDisplay(tk.Frame):
    """
    Multi-bit binary LED display.
    """

    def __init__(self, parent, bit_width=8, label="", **kwargs):
        """Initialize binary display with specified bit width."""
        super().__init__(parent, **kwargs)
        self.bit_width = bit_width
        self.leds = []

        # Label
        if label:
            tk.Label(self, text=label, font=("Arial", 10, "bold")).pack(side=tk.TOP)

        # LED container
        led_frame = tk.Frame(self)
        led_frame.pack()

        # Create LEDs (MSB to LSB for display)
        for i in range(bit_width - 1, -1, -1):
            led = BinaryLED(led_frame)
            led.pack(side=tk.LEFT, padx=2)
            self.leds.append(led)

        # Bit position labels
        label_frame = tk.Frame(self)
        label_frame.pack()
        for i in range(bit_width - 1, -1, -1):
            tk.Label(label_frame, text=str(i), font=("Arial", 8)).pack(
                side=tk.LEFT, padx=8)

        # Decimal value display
        self.decimal_label = tk.Label(self, text="Decimal: 0",
                                      font=("Arial", 9))
        self.decimal_label.pack()

    def set_binary(self, bits: list):
        """
        Set display from binary list (LSB first).

        Args:
            bits: List of bits (LSB first)
        """
        # Pad or truncate to bit width
        display_bits = bits[:self.bit_width] + [0] * (self.bit_width - len(bits))

        # Update LEDs (reverse for MSB first display)
        for i, led in enumerate(self.leds):
            bit_index = self.bit_width - 1 - i
            led.set_value(display_bits[bit_index] if bit_index < len(display_bits) else 0)

        # Update decimal value
        decimal = BinaryAnalyzer.binary_to_decimal(display_bits)
        self.decimal_label.config(text=f"Decimal: {decimal}")


class ArithmeticPanel(tk.Frame):
    """
    Panel for arithmetic operations with step-by-step execution.
    """

    def __init__(self, parent):
        """Initialize arithmetic panel."""
        super().__init__(parent, relief=tk.RAISED, borderwidth=2)
        self.arithmetic = BinaryArithmetic(bit_width=8)

        # Title
        tk.Label(self, text="Arithmetic Operations",
                 font=("Arial", 12, "bold")).pack(pady=5)

        # Input section
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Operand A:").grid(row=0, column=0, padx=5)
        self.entry_a = tk.Entry(input_frame, width=15)
        self.entry_a.grid(row=0, column=1, padx=5)
        self.entry_a.insert(0, "5")

        tk.Label(input_frame, text="Operand B:").grid(row=1, column=0, padx=5)
        self.entry_b = tk.Entry(input_frame, width=15)
        self.entry_b.grid(row=1, column=1, padx=5)
        self.entry_b.insert(0, "3")

        # Operation buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        operations = [
            ("ADD", self.do_add),
            ("SUB", self.do_sub),
            ("MUL", self.do_mul),
            ("DIV", self.do_div)
        ]

        for i, (op_name, cmd) in enumerate(operations):
            btn = tk.Button(btn_frame, text=op_name, command=cmd,
                            width=8, bg="#4CAF50", fg="white")
            btn.grid(row=0, column=i, padx=2)

        # Binary displays
        display_frame = tk.Frame(self)
        display_frame.pack(pady=10)

        self.display_a = BinaryDisplay(display_frame, label="Input A")
        self.display_a.pack()

        self.display_b = BinaryDisplay(display_frame, label="Input B")
        self.display_b.pack()

        self.display_result = BinaryDisplay(display_frame, label="Result", bit_width=16)
        self.display_result.pack()

        # Execution log
        tk.Label(self, text="Execution Trace:", font=("Arial", 10, "bold")).pack()
        self.log_text = scrolledtext.ScrolledText(self, height=12, width=60,
                                                  font=("Courier", 8))
        self.log_text.pack(pady=5, padx=10)

    def get_operands(self):
        """Get operands from entry fields."""
        try:
            a_val = int(self.entry_a.get())
            b_val = int(self.entry_b.get())

            if a_val < 0 or b_val < 0 or a_val > 255 or b_val > 255:
                messagebox.showerror("Error", "Values must be between 0 and 255")
                return None, None

            a_bits = BinaryAnalyzer.decimal_to_binary(a_val, 8)
            b_bits = BinaryAnalyzer.decimal_to_binary(b_val, 8)

            return a_bits, b_bits
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Enter integers only.")
            return None, None

    def update_displays(self, a_bits, b_bits, result_bits):
        """Update binary LED displays."""
        self.display_a.set_binary(a_bits)
        self.display_b.set_binary(b_bits)
        self.display_result.set_binary(result_bits)

    def show_trace(self):
        """Display execution trace in log."""
        self.log_text.delete(1.0, tk.END)

        for step in self.arithmetic.execution_steps:
            self.log_text.insert(tk.END, f"\n{'=' * 50}\n")
            self.log_text.insert(tk.END, f"{step['description']}\n")

            if step['data']:
                for key, value in step['data'].items():
                    self.log_text.insert(tk.END, f"  {key}: {value}\n")

        self.log_text.see(tk.END)

    def do_add(self):
        """Perform addition."""
        a_bits, b_bits = self.get_operands()
        if a_bits is None:
            return

        result, overflow = self.arithmetic.ripple_carry_adder(a_bits, b_bits, trace=True)
        self.update_displays(a_bits, b_bits, result)
        self.show_trace()

        if overflow:
            messagebox.showwarning("Overflow", "Addition overflow occurred!")

    def do_sub(self):
        """Perform subtraction."""
        a_bits, b_bits = self.get_operands()
        if a_bits is None:
            return

        result, borrow, _ = self.arithmetic.subtract(a_bits, b_bits, trace=True)
        self.update_displays(a_bits, b_bits, result)
        self.show_trace()

        if borrow:
            messagebox.showwarning("Underflow", "Subtraction underflow occurred!")

    def do_mul(self):
        """Perform multiplication."""
        a_bits, b_bits = self.get_operands()
        if a_bits is None:
            return

        result = self.arithmetic.multiply(a_bits, b_bits, trace=True)
        self.update_displays(a_bits, b_bits, result)
        self.show_trace()

    def do_div(self):
        """Perform division."""
        a_bits, b_bits = self.get_operands()
        if a_bits is None:
            return

        quotient, remainder = self.arithmetic.divide(a_bits, b_bits, trace=True)

        # Show both quotient and remainder
        self.update_displays(a_bits, b_bits, quotient)
        self.show_trace()

        rem_val = BinaryAnalyzer.binary_to_decimal(remainder)
        messagebox.showinfo("Division Result",
                            f"Remainder: {rem_val}\n"
                            f"Binary: {BinaryAnalyzer.format_binary_string(remainder)}")


class LogicDesignerPanel(tk.Frame):
    """
    Panel for custom logic expression evaluation and truth tables.
    """

    def __init__(self, parent):
        """Initialize logic designer panel."""
        super().__init__(parent, relief=tk.RAISED, borderwidth=2)
        self.parser = LogicExpressionParser()
        self.simulator = CircuitSimulator()

        # Title
        tk.Label(self, text="Logic Expression Evaluator",
                 font=("Arial", 12, "bold")).pack(pady=5)

        # Expression input
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Boolean Expression:").pack()
        tk.Label(input_frame, text="(Use: AND, OR, XOR, NOT, parentheses)",
                 font=("Arial", 8)).pack()

        self.expr_entry = tk.Entry(input_frame, width=40, font=("Arial", 11))
        self.expr_entry.pack(pady=5)
        self.expr_entry.insert(0, "(A AND B) OR NOT C")

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Generate Truth Table",
                  command=self.generate_truth_table,
                  bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Simulate Step-by-Step",
                  command=self.simulate_expression,
                  bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)

        # Output area
        tk.Label(self, text="Output:", font=("Arial", 10, "bold")).pack()
        self.output_text = scrolledtext.ScrolledText(self, height=20, width=70,
                                                     font=("Courier", 9))
        self.output_text.pack(pady=5, padx=10)

    def generate_truth_table(self):
        """Generate and display truth table."""
        expression = self.expr_entry.get().strip()
        if not expression:
            messagebox.showerror("Error", "Enter a Boolean expression")
            return

        try:
            truth_table = self.parser.generate_truth_table(expression)
            formatted = self.parser.format_truth_table(truth_table)

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, formatted)

        except Exception as e:
            messagebox.showerror("Error", f"Expression error: {str(e)}")

    def simulate_expression(self):
        """Simulate expression with step-by-step execution."""
        expression = self.expr_entry.get().strip()
        if not expression:
            messagebox.showerror("Error", "Enter a Boolean expression")
            return

        # Get variable values
        variables = self.parser.extract_variables(self.parser.tokenize(expression))

        if not variables:
            messagebox.showerror("Error", "No variables found in expression")
            return

        # Create dialog for variable input
        dialog = tk.Toplevel(self)
        dialog.title("Enter Variable Values")
        dialog.geometry("300x200")

        tk.Label(dialog, text="Enter values (0 or 1):",
                 font=("Arial", 10, "bold")).pack(pady=10)

        entries = {}
        for var in variables:
            frame = tk.Frame(dialog)
            frame.pack(pady=2)
            tk.Label(frame, text=f"{var}:").pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(frame, width=5)
            entry.pack(side=tk.LEFT)
            entry.insert(0, "0")
            entries[var] = entry

        def execute_sim():
            try:
                values = {}
                for var, entry in entries.items():
                    val = int(entry.get())
                    if val not in [0, 1]:
                        raise ValueError()
                    values[var] = val

                trace = self.simulator.simulate_step_by_step(expression, values)

                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"Expression: {expression}\n")
                self.output_text.insert(tk.END, f"Inputs: {values}\n\n")
                self.output_text.insert(tk.END, "=" * 60 + "\n")
                self.output_text.insert(tk.END, "EXECUTION TRACE\n")
                self.output_text.insert(tk.END, "=" * 60 + "\n\n")

                for entry in trace:
                    self.output_text.insert(tk.END, f"{entry['step']}: {entry['description']}\n")
                    for key, value in entry['data'].items():
                        self.output_text.insert(tk.END, f"  {key}: {value}\n")
                    self.output_text.insert(tk.END, "\n")

                dialog.destroy()

            except ValueError:
                messagebox.showerror("Error", "Enter only 0 or 1 for each variable")

        tk.Button(dialog, text="Execute", command=execute_sim,
                  bg="#4CAF50", fg="white").pack(pady=10)


class ALUPanel(tk.Frame):
    """
    Panel for ALU simulation with operation selection.
    """

    def __init__(self, parent):
        """Initialize ALU panel."""
        super().__init__(parent, relief=tk.RAISED, borderwidth=2)
        self.alu = ALU(bit_width=8)
        self.control = ControlUnit(self.alu)

        # Title
        tk.Label(self, text="Mini ALU Simulator",
                 font=("Arial", 12, "bold")).pack(pady=5)

        # Operation selection
        op_frame = tk.Frame(self)
        op_frame.pack(pady=10)

        tk.Label(op_frame, text="Select Operation:").pack()

        self.op_var = tk.StringVar(value="ADD")
        operations = ["ADD", "SUB", "MUL", "DIV", "AND", "OR", "XOR",
                      "NOT", "SHL", "SHR", "ROL", "ROR"]

        combo_frame = tk.Frame(op_frame)
        combo_frame.pack()

        self.op_combo = ttk.Combobox(combo_frame, textvariable=self.op_var,
                                     values=operations, state="readonly", width=15)
        self.op_combo.pack(side=tk.LEFT, padx=5)

        tk.Button(combo_frame, text="Execute", command=self.execute_operation,
                  bg="#4CAF50", fg="white", width=10).pack(side=tk.LEFT)

        # Input section
        input_frame = tk.Frame(self)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Operand A:").grid(row=0, column=0)
        self.alu_entry_a = tk.Entry(input_frame, width=12)
        self.alu_entry_a.grid(row=0, column=1, padx=5)
        self.alu_entry_a.insert(0, "15")

        tk.Label(input_frame, text="Operand B:").grid(row=1, column=0)
        self.alu_entry_b = tk.Entry(input_frame, width=12)
        self.alu_entry_b.grid(row=1, column=1, padx=5)
        self.alu_entry_b.insert(0, "7")

        # Result display
        self.alu_result_display = BinaryDisplay(self, label="ALU Result")
        self.alu_result_display.pack(pady=10)

        # Flags display
        flag_frame = tk.LabelFrame(self, text="Status Flags", font=("Arial", 10, "bold"))
        flag_frame.pack(pady=5, fill=tk.X, padx=10)

        self.flag_labels = {}
        flags = ["Zero", "Carry", "Overflow", "Sign", "Parity"]
        for i, flag in enumerate(flags):
            frame = tk.Frame(flag_frame)
            frame.pack(side=tk.LEFT, padx=10, pady=5)

            label = tk.Label(frame, text=flag, font=("Arial", 8))
            label.pack()

            value_label = tk.Label(frame, text="0", font=("Arial", 12, "bold"),
                                   fg="#808080", width=2)
            value_label.pack()

            self.flag_labels[flag] = value_label

        # Execution log
        tk.Label(self, text="ALU Execution Log:", font=("Arial", 10, "bold")).pack()
        self.alu_log = scrolledtext.ScrolledText(self, height=10, width=65,
                                                 font=("Courier", 8))
        self.alu_log.pack(pady=5, padx=10)

    def execute_operation(self):
        """Execute selected ALU operation."""
        try:
            a_val = int(self.alu_entry_a.get())
            b_val = int(self.alu_entry_b.get())

            if a_val < 0 or b_val < 0 or a_val > 255 or b_val > 255:
                messagebox.showerror("Error", "Values must be between 0 and 255")
                return

            a_bits = BinaryAnalyzer.decimal_to_binary(a_val, 8)
            b_bits = BinaryAnalyzer.decimal_to_binary(b_val, 8)

            # Map operation name to opcode
            op_map = {
                "ADD": ALU.OP_ADD, "SUB": ALU.OP_SUB, "MUL": ALU.OP_MUL,
                "DIV": ALU.OP_DIV, "AND": ALU.OP_AND, "OR": ALU.OP_OR,
                "XOR": ALU.OP_XOR, "NOT": ALU.OP_NOT, "SHL": ALU.OP_SHL,
                "SHR": ALU.OP_SHR, "ROL": ALU.OP_ROL, "ROR": ALU.OP_ROR
            }

            opcode = op_map[self.op_var.get()]

            instruction = {
                'opcode': opcode,
                'operand_a': a_bits,
                'operand_b': b_bits if self.op_var.get() != "NOT" else None
            }

            result = self.control.decode_and_execute(instruction, trace=True)

            # Update displays
            self.alu_result_display.set_binary(result)

            # Update flags
            flags = self.alu.flags.to_dict()
            for flag_name, value in flags.items():
                color = "#00FF00" if value == 1 else "#808080"
                self.flag_labels[flag_name].config(text=str(value), fg=color)

            # Show execution log
            self.alu_log.delete(1.0, tk.END)
            for entry in self.alu.execution_log:
                self.alu_log.insert(tk.END, f"\n{entry['description']}\n")
                for key, value in entry['data'].items():
                    self.alu_log.insert(tk.END, f"  {key}: {value}\n")

            self.alu_log.see(tk.END)

        except ValueError:
            messagebox.showerror("Error", "Invalid input")
        except Exception as e:
            messagebox.showerror("Error", f"Execution error: {str(e)}")


class MainApplication(tk.Tk):
    """
    Main application window with tabbed interface.
    """

    def __init__(self):
        """Initialize main application."""
        super().__init__()

        self.title("Intelligent Binary Logic Simulator and Calculator")
        self.geometry("900x700")

        # Create menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Usage Guide", command=self.show_usage)

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add tabs
        self.arithmetic_panel = ArithmeticPanel(self.notebook)
        self.notebook.add(self.arithmetic_panel, text="Arithmetic Operations")

        self.logic_panel = LogicDesignerPanel(self.notebook)
        self.notebook.add(self.logic_panel, text="Logic Designer")

        self.alu_panel = ALUPanel(self.notebook)
        self.notebook.add(self.alu_panel, text="ALU Simulator")

        # Status bar
        self.status_bar = tk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def show_about(self):
        """Show about dialog."""
        about_text = """
Intelligent Binary Logic Simulator and Calculator

An educational platform for understanding digital logic 
and arithmetic operations at the gate level.

Features:
• Gate-level arithmetic operations
• Interactive logic expression evaluator
• Mini ALU simulator with status flags
• Step-by-step execution visualization

Version: 1.0
        """
        messagebox.showinfo("About", about_text)

    def show_usage(self):
        """Show usage guide."""
        usage_text = """
USAGE GUIDE

Arithmetic Operations Tab:
- Enter decimal values (0-255)
- Click operation button (ADD, SUB, MUL, DIV)
- View step-by-step gate-level execution
- Binary LEDs show real-time results

Logic Designer Tab:
- Enter Boolean expressions using AND, OR, XOR, NOT
- Generate complete truth tables
- Simulate step-by-step evaluation

ALU Simulator Tab:
- Select operation from dropdown
- Enter operands
- Execute to see ALU operation
- View status flags and execution trace

Supported Operators:
AND, OR, XOR, NOT, parentheses ()
        """
        messagebox.showinfo("Usage Guide", usage_text)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()