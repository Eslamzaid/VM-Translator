import os
from Parser import Parser
from TranslationData import TransOptions


class Code_writer:
    def __init__(self, file_name) -> None:
        self.file_name = file_name

    def translate(self):
        __location__ = os.path.realpath(os.path.join(
            os.getcwd(), os.path.dirname(__file__)))
        parser = Parser()
        tsOption = TransOptions(self.file_name)
        try:
            f = open(os.path.join(__location__, self.file_name))
            w = open(os.path.join(__location__,
                     self.file_name[:-2]+"asm"), "w")
            for line in f.readlines():
                if not (line.strip().startswith("//") or line.startswith("\n")) and not len(line) == 0:
                    parser.setCommand(line.strip())
                    cp = parser.commandDestructure()
                    w.write("// "+line.strip()+"\n")
                    w.write(tsOption.addCommand(parser.command_Type, cp))
            f.close()
            w.close()
        except FileNotFoundError as e:
            raise FileExistsError("File does not exist")
        except:
            print("something went wrong")
            return 1
