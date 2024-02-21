import os
from Parser import Parser
from TranslationData import TransOptions


class Folder_Code_Writer:
    def __init__(self, folder_name) -> None:
        self.folder_name = folder_name

    def translate(self):
        __location__ = os.path.realpath(os.path.join(
            os.getcwd(), os.path.dirname(__file__), self.folder_name))
        openPath = os.path.join(os.path.split(__location__)[
                                0], self.folder_name+".asm")
        files = [f for f in os.listdir(__location__) if "vm" in f]
        parser = Parser()
        used = True
        try:
            w = open(openPath, "w")
            for file in files:
                tsOption = TransOptions(file)
                f = open(os.path.join(__location__, file), 'r')
                w.write("// ########## " + file + " ##########\n")
                for line in f.readlines():
                    if not (line.startswith("//") or line.startswith("\n")) and not len(line) == 0:
                        parser.setCommand(line.strip())
                        cp = parser.commandDestructure()
                        if used == True:
                            w.write(tsOption.addBootstrap(cp)+'\n')
                            used = False
                        w.write("// "+line.strip()+"\n")
                        w.write(tsOption.addCommand(parser.command_Type, cp))
                f.close()
            w.close()
        except FileNotFoundError as e:
            raise FileExistsError("File does not exist")
        except:
            print("something went wrong")
            return 1


# test = Folder_Code_Writer("Test")
# test.translate()
