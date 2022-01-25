class Delegate:
    def __init__(self):
        self.commands = []

    def __iadd__(self, func):
        self.commands.append(func)

    def invoke(self):
        if self.commands:
            for func in self.commands:
                func()
