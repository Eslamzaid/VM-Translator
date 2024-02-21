class Parser:
    def __init__(self) -> None:
        self.current_command = ''
        self.command_Type = ''
        self.command_data = None

    def setCommand(self, command):
        self.current_command = command
        parts = self.current_command.split()[:3]
        self.command_data = parts
        if 'p' in parts[0]:
            self.command_Type = "push_pop"
        elif len(parts[0]) <= 3:
            self.command_Type = "arithmetic_logic"
        elif 'if' in parts[0]:
            self.command_Type = "condition"
        elif parts[0] == "goto":
            self.command_Type = "jump"
        elif parts[0] == "label":
            self.command_Type = "label"
        elif parts[0] == "call":
            self.command_Type = "call"    
        elif parts[0] == "return":
            self.command_Type = "return"
        elif parts[0] == "function":
            self.command_Type = "function"

    def commandDestructure(self):
        if len(self.current_command) == 0:
            return "Cannot destructure an empty command"
        return self.command_data

    def getCommand(self):
        return self.current_command

    def getCommandType(self):
        return self.command_Type
