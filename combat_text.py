class CombatText():
    def __init__(self):
        self.text_lines = []

    def add_line(self, new_line):
        self.text_lines.append(new_line)

    def output(self):
        return '\n'.join(self.text_lines)
