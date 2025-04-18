import qtpy
from PyQt5.QtWidgets import QMainWindow, QWidget, QComboBox, QPushButton, QLineEdit, QDockWidget, QGridLayout, QLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from serialConnection import serialConnectionClass
from shapeManipulation import shapeManipulationClass
from connectionWindow import connectionWindowClass

class classUIinitialization(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1600, 900)        

        self.centralWidget = QWidget()
        self.serialConnectionDock = serialConnectionClass(self, self.centralWidget)
        self.shapeManiputationDock = shapeManipulationClass(self, self.centralWidget)
        self.connectionWindowDock = connectionWindowClass(self, self.centralWidget)

        self.dock_widgets = {
            "SerialConnection": {
                "widget": self.serialConnectionDock.serialConnectionFrontend,
                "area": Qt.LeftDockWidgetArea,
                "dock": None,
                "action": None
            },
            "ShapeManipulation": {
                "widget": self.shapeManiputationDock,
                "area": Qt.RightDockWidgetArea,
                "dock": None,
                "action": None
            },
            "ConnectionWindow": {
                "widget": self.connectionWindowDock,
                "area": Qt.LeftDockWidgetArea,
                "dock": None,
                "action": None
            }
        }     

        self.addDockWidgets()

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

    def add_dock_widgets(self):
        pass

    def create_menu_bar(self):
        pass
    
    def run(self):
        self.show()

    def add_to_layout(self, child, parent_layout, grid_row=0, grid_col=0, rowspan=0, colspan=0):
        if parent_layout is None:
            print("Error: parent_layout is None")
            return
        if isinstance(parent_layout, QGridLayout):
            if grid_row is None: grid_row = 0
            if grid_col is None: grid_col = 0
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

    def create_button(self, function, layout, name):
        button = QPushButton(name)
        button.clicked.connect(lambda: function())
        self.add_to_layout(button, layout)
        return button

    def create_combo_box(self, connect_function, layout):
        combo_box = QComboBox()
        combo_box.addItems([])
        combo_box.currentIndexChanged.connect(connect_function)
        self.add_to_layout(combo_box, layout)

        return combo_box 
