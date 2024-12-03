"""Create the hack file"""


class Writer:
    def __init__(self, path):
        """Creates the hack file"""
        self.path = path
        self.file = open(self.path, "w")

    def write_line(self, line):
        self.file.write(line + "\n")

    def __del__(self):
        self.file.close()
        print("Closing file:", self.path)
