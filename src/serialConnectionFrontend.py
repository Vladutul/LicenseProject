from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout
from functools import partial


class serialConnectionFrontend(QWidget):
    def __init__(self, parent, main_reference, container):
        super(serialConnectionFrontend, self).__init__(container)
        self.parent = parent
        self.main_reference = main_reference

        self.target_port = None
        self.init_UI()

    def init_UI(self):
        self.main_grid_layout = QGridLayout()
        self.label = QLabel()
        self.main_grid_layout.setSpacing(0)
        self.main_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_grid_layout.setRowStretch(0, 0)
        self.main_grid_layout.setRowStretch(1, 0)
        self.main_grid_layout.setColumnStretch(0, 0)

        self.horizontal_layout_first_row = QHBoxLayout()
        self.horizontal_layout_first_row.setSpacing(0)
        self.horizontal_layout_first_row.setContentsMargins(0, 0, 0, 0)

        self.horizontal_layout_second_row = QHBoxLayout()
        self.horizontal_layout_second_row.setSpacing(0)
        self.horizontal_layout_second_row.setContentsMargins(0, 0, 0, 0)

        self.vertical_layout_left = QVBoxLayout()
        self.vertical_layout_left.setSpacing(0)
        self.vertical_layout_left.setContentsMargins(0, 0, 0, 0)
        self.vertical_left_layout_container = QWidget()
        self.vertical_left_layout_container.setFixedWidth(100)  # Set your desired width
        self.vertical_left_layout_container.setLayout(self.vertical_layout_left)

        self.vertical_layout_right = QVBoxLayout()
        self.vertical_layout_right.setSpacing(0)
        self.vertical_layout_right.setContentsMargins(0, 0, 0, 0)
        self.vertical_right_layout_container = QWidget()
        self.vertical_right_layout_container.setFixedWidth(100)  # Set your desired width
        self.vertical_right_layout_container.setLayout(self.vertical_layout_right)

        self.main_reference.add_to_layout(self.vertical_left_layout_container, self.main_grid_layout, 0, 0, 4, 1)
        self.main_reference.add_to_layout(self.horizontal_layout_first_row, self.main_grid_layout, 0, 2, 1, 6)
        self.main_reference.add_to_layout(self.horizontal_layout_second_row, self.main_grid_layout, 1, 2, 1, 6)
        self.main_reference.add_to_layout(self.vertical_right_layout_container, self.main_grid_layout, 0, 1, 4, 1)

        self.buttons = {}
        self.combo_box = self.main_reference.create_combo_box(self.selection_changed, self.horizontal_layout_first_row)
        self.serialConnectionFronted_buttons_init()
        self.g_commands_buttons_wrapper()
        self.serial_commands_textbox = self.main_reference.create_text_box(self.horizontal_layout_second_row)
        
        self.setLayout(self.main_grid_layout)
        self.main_grid_layout.setColumnStretch(0, 1)  # left
        self.main_grid_layout.setColumnStretch(1, 4)  # center
        self.main_grid_layout.setColumnStretch(2, 1)  # right


    def g_commands_buttons_wrapper(self):
        left_vertical_row_button_dictionary = [
            ("G91", partial(self.send_gcode_command_wrapper, "G91"), "Send G91"),
            ("G90", partial(self.send_gcode_command_wrapper, "G90"), "Send G90"),
            ("M3", partial(self.send_gcode_command_wrapper, "M3"), "Send M3"),
            ("M4", partial(self.send_gcode_command_wrapper, "M4"), "Send M4"),
            ("M5", partial(self.send_gcode_command_wrapper, "M5"), "Send M5"),
            ("Reset", self.reset_connection, "Reset")
        ]

        self.buttons_creation_wrapper(left_vertical_row_button_dictionary, self.vertical_layout_left)
    
        right_vertical_row_button_dictionary = [
            ("G1 x10 F400", partial(self.send_gcode_command_wrapper, "G1 x10 F400"), "Send G1 x10 F400"),
            ("G1 x-10 F400", partial(self.send_gcode_command_wrapper, "G1 x-10 F400"), "Send G1 x-10 F400"),
            ("G1 y10 F400", partial(self.send_gcode_command_wrapper, "G1 y10 F400"), "Send G1 y10 F400"),
            ("G1 y-10 F400", partial(self.send_gcode_command_wrapper, "G1 y-10 F400"), "Send G1 y-10 F400"),
            ("G1 z10 F400", partial(self.send_gcode_command_wrapper, "G1 z10 F400"), "Send G1 z10 F400"),
            ("G1 z-10 F400", partial(self.send_gcode_command_wrapper, "G1 z-10 F400"), "Send G1 z-10 F400")
        ]

        self.buttons_creation_wrapper(right_vertical_row_button_dictionary, self.vertical_layout_right)

    def reset_connection(self):
        self.parent.serialConnectionBackend.reset_connection()

    def serialConnectionFronted_buttons_init(self):
        first_horizontal_row_button_dictionary = [
            ("update", self.update_combo_box, "Update"),
            ("connect", self.connect_to_port, "Connect"),
            ("send", self.send_data_wrapper, "Send"),
            ("read", self.thread_read_data_wrapper, "Read"),
            ("stop", self.stop_reading_wrapper, "Stop"),
        ]

        self.buttons_creation_wrapper(first_horizontal_row_button_dictionary, self.horizontal_layout_first_row)

    def buttons_creation_wrapper(self, button_dictionary, layout):
        for key, callback, label in button_dictionary:
            self.buttons[key] = self.main_reference.create_button(callback, layout, label)

    def get_command_from_textbox(self):
        return self.serial_commands_textbox.text()

    def send_gcode_command_wrapper(self, command):
        if self.target_port:
            self.parent.serialConnectionBackend.send_data(command)

    def send_data_wrapper(self):
        print(self.get_command_from_textbox())
        #self.parent.serialConnectionBackend.send_data(self.get_command_from_textbox())
        if self.target_port:
            self.parent.serialConnectionBackend.send_data(self.get_command_from_textbox())

    def thread_read_data_wrapper(self):
        self.parent.serialConnectionBackend.thread_read_data()

    def stop_reading_wrapper(self):
        self.parent.serialConnectionBackend.stop_reading()

    def update_combo_box(self):
        ports = self.find_ports()
        self.combo_box.clear()
        self.combo_box.addItems(ports)

    def return_target_port(self):
        return self.target_port

    def selection_changed(self):
        selected_port = self.combo_box.currentText()
        self.label.setText(f"Port: {selected_port}")
        self.target_port = selected_port

    def find_ports(self):
        return self.parent.find_ports() if hasattr(self.parent, "find_ports") else []

    def connect_to_port(self):
        self.parent.serialConnectionBackend.connect_to_port()