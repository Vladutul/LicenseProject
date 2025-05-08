from PyQt5.QtWidgets import QMainWindow, QWidget, QComboBox, QPushButton, QAction, QLineEdit, QDockWidget, QGridLayout, QLayout, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from serialConnection import serialConnectionClass
from shapeManipulation import shapeManipulationClass
from connectionWindow import connectionWindowClass
from gCodeGeneration import gCodeGenerationClass


class classUIinitialization(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1600, 900)        

        self.serialConnectionDock = serialConnectionClass(self, None)
        self.shapeManiputationDock = shapeManipulationClass(self, None)
        self.connectionWindowDock = connectionWindowClass(self, None)
        self.gCodeGeneration = gCodeGenerationClass(self, None)

        self.dock_generation()
        self.addDockWidgets()
        self.createMenuBar()

    def dock_generation(self):
        self.dock_widgets = {
            "SerialConnection": {
                "widget": self.serialConnectionDock.serialConnectionFrontend,
                "area": Qt.RightDockWidgetArea,
                "dock": None,
                "action": None
            },
            "ShapeManipulation": {
                "widget": self.shapeManiputationDock,
                "area": Qt.LeftDockWidgetArea,
                "dock": None,
                "action": None
            },
            "ConnectionWindow": {
                "widget": self.connectionWindowDock,
                "area": Qt.RightDockWidgetArea,
                "dock": None,
                "action": None
            }
        }

    def addDockWidgets(self):
        for dockName, info in self.dock_widgets.items():
            dock = self.createDockWidget(dockName, info["widget"])
            self.addDockWidget(info["area"], dock)
            info["dock"] = dock  # Store reference to dock widget

    def createDockWidget(self, dockName, widget):
        dock = QDockWidget(dockName, self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        dock.setWidget(widget)
        dock.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        dock.visibilityChanged.connect(lambda visible, t=dockName: self.onDockVisibilityChanged(t, visible))
        self.setDockOptions(QMainWindow.AllowNestedDocks | QMainWindow.AllowTabbedDocks | QMainWindow.AnimatedDocks)

        return dock

    def onDockVisibilityChanged(self, title, visible):
        dock_info = self.dock_widgets.get(title)
        
        if dock_info:
            action = dock_info["action"]
            if action:
                action.setChecked(visible)

    def createMenuBar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        view_menu = menu_bar.addMenu('View')
        #help_menu = menu_bar.addMenu('Help')

        #file_menu
        open_saved_project = QAction('Open Project', self)
        open_saved_project.setStatusTip('Open a saved project')
        #open_action.triggered.connect(self.dataset_treeview.open_file)

        generate_gCode = QAction('Generate GCode', self)
        generate_gCode.setStatusTip('Generate GCode')
        #open_bar_view_action.triggered.connect(self.dataset_treeview.open_file_adc2)

        exit_action = QAction('Exit', self)
        exit_action.setStatusTip('Exit the application')
        #exit_action.triggered.connect(self.close)

        #view_menu
        for title, info in self.dock_widgets.items():
            action = QAction(title, self, checkable=True)
            action.setChecked(True)  # Initially checked
            action.triggered.connect(lambda checked, t=title: self.toggleDockWidget(t, checked))
            view_menu.addAction(action)
            self.dock_widgets[title]["action"] = action

        file_menu.addAction(open_saved_project)
        file_menu.addAction(generate_gCode)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        #help_menu
        #test_button_action = QAction('Test_Button', self)
        #test_button_action.triggered.connect()
        #help_menu.addAction(test_button_action)
    
    def toggleDockWidget(self, title, checked):
        dock = self.dock_widgets[title]["dock"]
        if dock:
            if checked:
                dock.show()
            else:
                dock.hide()

    def onDockVisibilityChanged(self, title, visible):
        dock_info = self.dock_widgets.get(title)
        if dock_info:
            action = dock_info["action"]
            if action:
                action.setChecked(visible)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit Confirmation', 
                                     "Are you sure you want to quit?", 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("Application is closing.")
            event.accept()
        else:
            event.ignore()

    def run(self):
        self.show()

    def add_to_layout(self, child, parent_layout, grid_row=0, grid_col=0, rowspan=0, colspan=0):
        if parent_layout is None:
            print("Error: parent_layout is None")
            return

        if isinstance(parent_layout, QGridLayout):
            if grid_row is None: grid_row = 0
            if grid_col is None: grid_col = 0
            if rowspan == 0: rowspan = 1
            if colspan == 0: colspan = 1
            if isinstance(child, QLayout):
                parent_layout.addLayout(child, grid_row, grid_col, rowspan, colspan)
            elif isinstance(child, QWidget):
                parent_layout.addWidget(child, grid_row, grid_col, rowspan, colspan)
            else:
                print("Error: child is neither QLayout nor QWidget")

        elif isinstance(parent_layout, (QHBoxLayout, QVBoxLayout)):
            if isinstance(child, QLayout):
                parent_layout.addLayout(child)
            elif isinstance(child, QWidget):
                parent_layout.addWidget(child)
            else:
                print("Error: child is neither QLayout nor QWidget")

    def create_text_box(self, layout):
        textbox = QLineEdit()
        textbox.move(20, 20)
        textbox.resize(280, 40)
        self.add_to_layout(textbox, layout)
        return textbox

    def create_button(self, function, layout, name, row=0, col=0):
        button = QPushButton(name)
        button.clicked.connect(lambda: function())
        self.add_to_layout(button, layout, row, col)
        return button

    def create_combo_box(self, connect_function, layout):
        combo_box = QComboBox()
        combo_box.addItems([])
        combo_box.currentIndexChanged.connect(connect_function)
        self.add_to_layout(combo_box, layout)

        return combo_box 
