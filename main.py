from assembler import Assembler

input_path = "/Users/yoav/Downloads/Rect.asm"
output_path = input_path.split("/")[-1].split(".")[0] + ".hack"

assembler = Assembler(input_file=input_path, output_file=output_path)
assembler.translate()

