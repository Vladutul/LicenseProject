from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout


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


        self.main_reference.add_to_layout(self.horizontal_layout_first_row, self.main_grid_layout, 0, 0, 1, 1)
        self.main_reference.add_to_layout(self.horizontal_layout_second_row, self.main_grid_layout, 1, 0, 1, 1)
        self.combo_box = self.main_reference.create_combo_box(self.selection_changed, self.horizontal_layout_first_row)
        self.update_button = self.main_reference.create_button(self.update_combo_box, self.horizontal_layout_first_row,"update")
        self.connect_button = self.main_reference.create_button(self.connect_to_port, self.horizontal_layout_first_row,"connect")
        self.send_command_button = self.main_reference.create_button(self.send_data_wrapper, self.horizontal_layout_first_row,"send")
        self.read_data_button = self.main_reference.create_button(self.thread_read_data_wrapper, self.horizontal_layout_first_row,"read")
        self.read_data_button = self.main_reference.create_button(self.stop_reading_wrapper, self.horizontal_layout_first_row,"stop")
        self.serial_commands_textbox = self.main_reference.create_text_box(self.horizontal_layout_second_row)
        
        self.setLayout(self.main_grid_layout)

    def get_command_from_textbox(self):
        return self.serial_commands_textbox.text()

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