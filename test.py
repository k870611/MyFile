import os
import re


def alter():
    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "z.txt")
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if "print" in line and "print(" not in line:
                line = re.sub(r'print\s*', "print(", line)
                if not line.endswith(")"):
                    line = line.replace('\n', ')\n')

            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


alter()
