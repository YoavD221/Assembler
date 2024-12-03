from parser import Parser, A_COMMAND, C_COMMAND, L_COMMAND
from symboltable import SymbolTable
from code import Code
from writer import Writer


class Assembler:

    def __init__(self, input_file, output_file):
        self.asm_file = Parser(input_file)
        self.hack_file = Writer(output_file)
        self.symbol_table = SymbolTable()
        self.code = Code()
        self.next_available_address = 16
    def translate(self):
        # First pass: record label locations
        program_counter = 0
        while self.asm_file.has_more_commands():
            line = self.asm_file.advance()
            if not line:  # Skip if line is None or empty
                continue

            command_type = self.asm_file.command_type()

            if command_type == L_COMMAND:
                # Add the label and its address to symbol table
                symbol = self.asm_file.symbol()
                self.symbol_table.add_entry(symbol, program_counter)
            elif command_type in [A_COMMAND, C_COMMAND]:
                # Only increment for actual instructions
                program_counter += 1

        # Reset for second pass
        self.asm_file = Parser(self.asm_file.path)

        # Second pass: translate instructions
        while self.asm_file.has_more_commands():
            line = self.asm_file.advance()
            if not line:
                continue

            command_type = self.asm_file.command_type()

            if command_type == L_COMMAND:
                continue

            if command_type == A_COMMAND:
                symbol = self.asm_file.symbol()
                if not symbol.isdigit():
                    address = self.symbol_table.get_address(symbol)
                else:
                    address = int(symbol)
                binary_line = '0' + format(address, '015b')

            elif command_type == C_COMMAND:
                dest = self.asm_file.dest()
                comp = self.asm_file.comp()
                jump = self.asm_file.jump()
                binary_line = "111" + self.code.comp(comp) + self.code.dest(dest) + self.code.jump(jump)

            self.hack_file.write_line(binary_line)
