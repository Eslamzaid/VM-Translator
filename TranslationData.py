import os


class TransOptions:
    cn = 0
    fp = "@SP\nAM=M-1\nD=M\n"
    lp = "@SP\nM=M+1"
    r_l_c = 0  # return label counter
    c_l_c = 0  # call address

    def __init__(self, filename) -> None:
        self.file_name = filename

    # ! ~ Minimize the string of those

    def pushPopCommand(self, cT, loc, value):
        name = os.path.basename(self.file_name[:-2])
        if cT == "push":
            if loc == "constant":
                return f"@{value}\nD=A\n"+"@SP\nA=M\nM=D\n"+self.lp
            elif loc == "static":
                return f"@{name+value}\nD=M\n@SP\nA=M\nM=D\n"+self.lp
            elif loc == "temp":
                return f"@{(5+int(value))}\nD=M\n@SP\nA=M\nM=D\n"+self.lp
            elif loc == "pointer":
                if int(value) == 0:
                    return "@THIS\nD=M\n@SP\nA=M\nM=D\n"+self.lp
                else:
                    return "@THAT\nD=M\n@SP\nA=M\nM=D\n"+self.lp
            else:
                return f"@{loc}\nD=M\n@{value}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n"+self.lp

        else:
            if loc == "temp":
                return f"{self.fp}@{(5+int(value))}\nM=D"
            elif loc == "static":
                return f"{self.fp}@{name+value}\nM=D"
            elif loc == "pointer":
                if int(value) == 0:
                    return f"{self.fp}@THIS\nM=D"
                else:
                    return f"{self.fp}@THAT\nM=D"
            return f"@{loc}\nD=M\n@{value}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"

    def arithCommand(self, cT):
        if cT == "add":
            return self.fp+"@SP\nAM=M-1\nM=M+D\n"+self.lp
        elif cT == "sub":
            return self.fp+"@SP\nAM=M-1\nM=M-D\n"+self.lp
        elif cT == "neg":
            return "@SP\nAM=M-1\nM=-M\n"+self.lp

    def comparisonCommand(self, cT):
        self.cn += 1
        nTs = self.cn
        if cT == "eq":
            return f"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=D-M\n@equal0{nTs}\nD;JEQ\n@SP\nA=M\nM=0\n@add1ToSP{nTs}\n0;JMP\n(equal0{nTs})\n@SP\nA=M\nM=-1\n(add1ToSP{nTs})\n"+self.lp
        elif cT == "gt":
            return f"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@equal0{nTs}\nD;JGT\n@SP\nA=M\nM=0\n@add1ToSP{nTs}\n0;JMP\n(equal0{nTs})\n@SP\nA=M\nM=-1\n(add1ToSP{nTs})\n"+self.lp
        elif cT == "lt":
            return f"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@equal0{nTs}\nD;JLT\n@SP\nA=M\nM=0\n@add1ToSP{nTs}\n0;JMP\n(equal0{nTs})\n@SP\nA=M\nM=-1\n(add1ToSP{nTs})\n"+self.lp

    def logicalCommand(self, cT):
        if cT == "and":
            return "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M&D\n"+self.lp
        elif cT == "or":
            return "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M|D\n"+self.lp
        elif cT == "not":
            return "@SP\nAM=M-1\nM=!M\n"+self.lp

    def getType(self, segment_name):
        name_mapping = {
            "constant": "constant",
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "temp": "temp",
            "pointer": "pointer",
            "static": "static",
            "add": "add",
            "sub": "sub",
            "neg": "neg",
            "eq": "eq",
            "gt": "gt",
            "lt": "lt",
            "and": "and",
            "or": "or",
            "not": "not"
        }
        return name_mapping.get(segment_name, "could not found anything")

    def addBootstrap(self):
        return "@SP\ncall Sys.init\n"+self.lp

    def functionCommand(self, cp):
        num = int(cp[2])
        result = f"({cp[1]})\n@SP\nD=M\n@LCL\nM=D\n"
        if num > 0:
            result += f"@{num}\nD=A\n@SP\nM=M+D\n"
        return result

    def returnCommand(self):
        result = f"@LCL\nD=M\n@endFrameAddress.{self.r_l_c}\nM=D\n@5\nA=D-A\nD=M\n@retAddress.{self.r_l_c}\nM=D\n@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\nD=A\n@SP\nM=D+1\n"
        for ms in ["THAT", "THIS", "ARG", "LCL"]:
            result += f"@endFrameAddress.{self.r_l_c}\nD=M-1\nAM=D\nD=M\n@{ms}\nM=D\n"
        result += f"@retAddress.{self.r_l_c}\nA=M\n0;JMP\n"
        self.r_l_c += 1
        return result

    def callCommand(self, cp):
        return f"@return_address.{self.c_l_c}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\nD=M\n@SP\nA=M\
            \nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THIS\nD=M\n@SP\nA=M\
            \nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nD=M\n@5\nD=D-A\n@{cp[2]}\nD=D-A\n@ARG\nM=D\
            \n@SP\nD=M\n@LCL\nM=D\n@{cp[1]}\n0;JMP\n(return_address.{self.c_l_c})\n"

    def addCommand(self, commandType, cp):
        if commandType == "push_pop":
            typ = self.getType(cp[1])
            return (self.pushPopCommand(
                cp[0], typ, cp[2])+"\n")
        elif commandType == "arithmetic_logic":
            typ = self.getType(cp[0])
            if typ in ["add", "sub", "neg"]:
                return self.arithCommand(typ)+"\n"
            elif typ in ["eq", "gt", "lt"]:
                return self.comparisonCommand(typ)+"\n"
            elif typ in ["and", "or", "not"]:
                return self.logicalCommand(typ)+"\n"
        elif commandType == "condition":
            return f"@SP\nM=M-1\nA=M\nD=M\nM=M+1\n@{cp[1]}\nD;JNE\n"
        elif commandType == "label":
            return f"({cp[1]})\n"
        elif commandType == "jump":
            return f"@{cp[1]}\n0;JMP\n"
        elif commandType == "function":
            return self.functionCommand(cp)
        elif commandType == "return":
            return self.returnCommand()
        elif commandType == "call":
            return self.callCommand(cp)
