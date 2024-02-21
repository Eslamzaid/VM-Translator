from CodeWriter import Code_writer
from FolderCodeWriter import Folder_Code_Writer
import sys
import os


def main():
    if len(sys.argv) < 2:
        return print("No file to read")
    f_name = sys.argv[1]
    if f_name.__contains__(".vm"):
        writer = Code_writer(f_name)
        writer.translate()
    elif '.' not in f_name:
        f_writer = Folder_Code_Writer(f_name)
        f_writer.translate()
    else:
        raise FileNotFoundError("File doesn't exist!")


if __name__ == "__main__":
    main()
