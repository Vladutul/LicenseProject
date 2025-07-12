from PyQt5.QtWidgets import QMainWindow, QWidget, QComboBox, QFileDialog, QPushButton, QAction, QLineEdit, QDockWidget, QGridLayout, QLayout, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from saveAndLoad import SaveAndLoadProjectClass
from serialConnection import serialConnectionClass
from shapeManipulation import shapeManipulationClass
from connectionWindow import connectionWindowClass
from gCodeGeneration import gCodeGenerationClass


class classUIinitialization(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1600, 900)
        self.setWindowTitle("LicenseProject")        

        self.filepath = None
        self.project_filepath = None
        self.serialConnectionDock = serialConnectionClass(self, None)
        self.shapeManiputationDock = shapeManipulationClass(self, None)
        self.connectionWindowDock = connectionWindowClass(self, None)
        self.gCodeGeneration = gCodeGenerationClass(self.shapeManiputationDock.plot_shapes_values_dictionary)
        self.saveAndLoadRefference = SaveAndLoadProjectClass(self.shapeManiputationDock.plot_shapes_values_dictionary)


        self.dock_generation()
        self.addDockWidgets()
        self.createMenuBar()

    def gCode_generation_wrapper_new_filepath(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save GCode File",
            "",
            "GCode Files (*.gcode);;All Files (*)",
            options=options
        )

        if filepath:
            self.filepath = filepath
            self.gCodeGeneration.gcode_file_path = self.filepath
            self.gCodeGeneration.create_gCode_file()
            print(f"GCode file saved to: {self.filepath}")
        else:
            print("File save operation canceled.")
    
    def gCode_generation_wrapper_existing_file(self):
        if self.filepath:
            self.gCodeGeneration.create_gCode_file()
        else:
            self.gCode_generation_wrapper_new_filepath()

    def save_project(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.project_filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project File",
            "",
            "Project Files (*.json);;All Files (*)",
            options=options
        )

        if self.project_filepath:
            self.saveAndLoadRefference.save_project(self.project_filepath)
            print(f"Project saved to: {self.project_filepath}")
            
    def open_project(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.project_filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project File",
            "",
            "Project Files (*.json);;All Files (*)",
            options=options
        )

        current_dict = self.shapeManiputationDock.plot_shapes_values_dictionary
        if current_dict and len(current_dict) > 0:
            reply = QMessageBox.question(
                self,
                "Unsaved Project",
                "You have unsaved changes. Do you want to save the current project before opening a new one?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if reply == QMessageBox.Yes:
                self.save_project()
            elif reply == QMessageBox.Cancel:
                return 

        if self.project_filepath:
            self.shapeManiputationDock.plot_shapes_values_dictionary.clear()
            self.saveAndLoadRefference.open_project(self.project_filepath)

        self.shapeManiputationDock.plotManager.clear_plot()
        self.shapeManiputationDock.plotManager.update_plot()

    def GCodeSendingWrapper(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open GCode File",
            "",
            "GCode Files (*.gcode);;All Files (*)",
            options=options
        )

        if filepath:
            self.serialConnectionDock.serialConnectionBackend.send_gcode_file(filepath)
            print(f"GCode file sent: {filepath}")
        else:
            print("File open operation canceled.")

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
                "area": Qt.BottomDockWidgetArea,
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
            info["dock"] = dock

            if dockName == "ConnectionWindow":
                dock.hide()
                info["action"] = None 

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
        open_project = QAction('Open Project', self)
        open_project.setStatusTip('Open a saved project')
        open_project.triggered.connect(self.open_project)

        save_project = QAction('Save Project', self)
        save_project.setStatusTip('Save the current project')
        save_project.triggered.connect(self.save_project)

        generate_gCode_existing_filepath = QAction('Generate GCode', self)
        generate_gCode_existing_filepath.setStatusTip('Generate GCode')
        generate_gCode_existing_filepath.triggered.connect(self.gCode_generation_wrapper_existing_file)

        generate_gCode_new_filepath = QAction('Generate GCode New File', self)
        generate_gCode_new_filepath.setStatusTip('Generate GCode New Filepath')
        generate_gCode_new_filepath.triggered.connect(self.gCode_generation_wrapper_new_filepath)

        send_gCode = QAction('Send GCode', self)
        send_gCode.setStatusTip('Send GCode to Arduino')
        send_gCode.triggered.connect(self.GCodeSendingWrapper)

        exit_action = QAction('Exit', self)
        exit_action.setStatusTip('Exit the application')
        #exit_action.triggered.connect(self.close)

        #view_menu
        for title, info in self.dock_widgets.items():
            action = QAction(title, self, checkable=True)
            if title == "ConnectionWindow":
                action.setChecked(False)
            else:
                action.setChecked(True)
            action.triggered.connect(lambda checked, t=title: self.toggleDockWidget(t, checked))
            view_menu.addAction(action)
            self.dock_widgets[title]["action"] = action

        file_menu.addAction(open_project)
        file_menu.addAction(save_project)
        file_menu.addAction(generate_gCode_existing_filepath)
        file_menu.addAction(generate_gCode_new_filepath)
        file_menu.addAction(send_gCode)
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
        textbox.setFixedWidth(600)
        textbox.setFixedHeight(40)
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
