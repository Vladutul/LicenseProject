from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout


class connectionWindowClass(QWidget):
    def __init__(self, parent, container):
        super(connectionWindowClass, self).__init__(container)

        self.main_grid_layout = QHBoxLayout()

        self.label = QLabel("connectionWindowClass")
        self.main_grid_layout.addWidget(self.label)

        self.setLayout(self.main_grid_layout)
