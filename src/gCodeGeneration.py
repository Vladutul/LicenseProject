

class gCodeGenerationClass:
    def __init__(self, gcode_file_path, real_values_dictionary):
        self.real_values_dictionary = real_values_dictionary

        self.gcode_file_path = gcode_file_path
        self.gcode_lines = []

    def generate_gcode(self, commands):
        for command in commands:
            self.gcode_lines.append(command)

    def save_gcode(self):
        with open(self.gcode_file_path, 'w') as file:
            for line in self.gcode_lines:
                file.write(line + '\n')