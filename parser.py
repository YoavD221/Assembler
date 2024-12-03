A_COMMAND = 0
C_COMMAND = 2
L_COMMAND = 4


class Parser:
    """Read and parses an instruction"""

    def __init__(self, path):
        self.current_command = None
        self.path = path
        self.file = open(self.path)
        self.lines = self.file.readlines()
        self.index = -1  # Line index of the file (including empty spaces)
        self.line_index = 0  # Line index of the instructions (not including empty spaces)
        self.line = None

    def __str__(self):
        return self.line

    def __len__(self):
        return len(self.line)

    def has_more_commands(self):
        """Returns true if there are more commands in the file."""
        return self.index + 1 < len(self.lines)

    def advance(self):
        """Reads the next instruction from the file and makes it the current instruction."""
        self.line = self.get_next_line()
        while self.line and len(self.line) == 0:  # Skip empty lines
            if not self.has_more_commands():
                return None
            self.line = self.get_next_line()

        if self.command_type() != L_COMMAND:
            self.line_index += 1

        return self.line

    def get_next_line(self):
        """Gets the next line, removing comments and whitespace."""
        self.index += 1
        if self.index >= len(self.lines):
            return None
        dirty_line = self.lines[self.index]
        return dirty_line.split("//")[0].strip()  # Remove whitespace and comments

    def command_type(self):
        """Returns the type of the current command."""
        if not self.line:
            return None
        if self.line[0] == "@":
            return A_COMMAND
        elif self.line[0] == "(" and self.line[-1] == ")":
            return L_COMMAND
        else:
            return C_COMMAND

    def symbol(self):
        """Returns the symbol or decimal xxx of the current command.
        Should be called only when command_type is A_COMMAND or L_COMMAND"""
        if self.command_type() == A_COMMAND:
            return self.line[1:]
        elif self.command_type() == L_COMMAND:
            return self.line[1:-1]

    def dest(self):
        """Returns the symbolic dest part of the current C-instruction.
        Should be called only when command_type is C_COMMAND"""
        if "=" in self.line:
            return self.line.split("=")[0]
        return None

    def comp(self):
        """Returns the symbolic comp part of the current C-instruction.
        Should be called only when command_type is C_COMMAND"""
        comp = self.line
        if "=" in comp:
            comp = comp.split("=")[1]
        if ";" in comp:
            comp = comp.split(";")[0]
        return comp

    def jump(self):
        """Returns the symbolic jump part of the current C-instruction.
        Should be called only when command_type is C_COMMAND"""
        if ";" in self.line:
            return self.line.split(";")[1]
        return None