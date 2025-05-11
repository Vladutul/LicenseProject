

class gCodeGenerationClass:
    def __init__(self, gcode_file_path, plot_shapes_values_dictionary):
        self.plot_shapes_values_dictionary = plot_shapes_values_dictionary

        drill_head_diameter = 0.5
        drill_head_height = 0.5
        drill_time_needed_to_drill_in_miliseconds = 0.5

        self.gcode_file_path = "C:/Users/Vladutul/Documents/FisierTestgCodeLicenta/output.gcode"
        self.gcode_lines = []

    def create_gCode_file(self):
        for key, data in self.plot_shapes_values_dictionary.items():
            gCode_text = None
            
            if data.get('shape') == 'paralelipiped':
                real_values = data.get('real_values', [])
                gCode_text = self.processed_drill_parallelepiped_data(*real_values[:-1])
                
            elif data.get('shape') == 'roundHole':
                pass

            elif data.get('shape') == 'drillPlate':
                pass
            
            if gCode_text:
                with open(self.gcode_file_path, 'w') as file:
                    file.write(gCode_text)

    
    def backup_gcode(self):
        xmin = float(10)
        xmax = float(50)
        ymin = float(20)
        ymax = float(60)
        zmin = float(0)
        zmax = float(5)

        gCode_text = self.generate_gCode(xmin, xmax, ymin, ymax, zmin, zmax)

        with open(self.gcode_file_path, 'w') as file:
            file.write(gCode_text)


    def processed_drill_parallelepiped_data(self, xmin, xmax, ymin, ymax, zmin, zmax, z_step=1.0, feed_xy=1000, feed_z=300):
        gcode = []
        gcode.append("G21 ; Set units to mm")
        gcode.append("G90 ; Absolute positioning")
        gcode.append("G1 Z5 F500 ; Raise to safe height")
        gcode.append(f"G0 X{xmin} Y{ymin} ; Move to starting XY")

        z = zmin
        while z <= zmax:
            gcode.append(f"G1 Z{z:.2f} F{feed_z} ; Lower to Z={z:.2f}")
            gcode.append(f"G1 X{xmax} Y{ymin} F{feed_xy}")
            gcode.append(f"G1 X{xmax} Y{ymax}")
            gcode.append(f"G1 X{xmin} Y{ymax}")
            gcode.append(f"G1 X{xmin} Y{ymin}")
            z += z_step

        gcode.append(f"G1 Z{zmax + 5:.2f} F{feed_z} ; Raise to safe Z")
        gcode.append("G0 X0 Y0 ; Home")
        gcode.append("M2 ; End program")
        
        return "\n".join(gcode)

    def save_gcode(self):
        with open(self.gcode_file_path, 'w') as file:
            for line in self.gcode_lines:
                file.write(line + '\n')