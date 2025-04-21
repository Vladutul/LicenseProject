from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea, QPushButton
import pyqtgraph.opengl as gl
import numpy as np
from miniFigure import createMiniFigure

class shapeManipulationClass(QWidget):
    def __init__(self, parent, container):
        super(shapeManipulationClass, self).__init__(container)
        self.drill_diameter = 0
        self.parent = parent
        self.input_boxes = {}
        self.plot_shapes_values_dictionary = {}
        self.mini_instances = []

        self.init_UI()
        self.init_plot()

    def init_UI(self):
        self.main_grid_layout = QGridLayout()
        self.buttons_horizontal_layout_first_row = QHBoxLayout()

        self.plot_container_widget = QWidget()
        self.plot_container_layout = QGridLayout()

        self.left_vertical_mini_widget = QWidget()
        self.vertical_mini_layout = QVBoxLayout()

        # Conține casetele + ploturile ca un widget orizontal
        self.inside_vertical_mini_layout = QHBoxLayout()

        # Adaugă butoanele în layoutul principal
        self.parent.add_to_layout(self.buttons_horizontal_layout_first_row, self.main_grid_layout, 0, 0, 1, 9)

        # Container pentru plotul 3D mare
        self.plot_container_widget.setLayout(self.plot_container_layout)
        self.parent.add_to_layout(self.plot_container_widget, self.main_grid_layout, 2, 2, 7, 7)

        # Crează un QScrollArea pentru a face widget-ul mini scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Allow resizing of the content inside the scroll area
        self.scroll_area.setWidget(self.left_vertical_mini_widget)

        # Adaugă scroll_area în layoutul principal
        self.parent.add_to_layout(self.scroll_area, self.main_grid_layout, 2, 0, 7, 2)

        # Container pentru mini
        self.left_vertical_mini_widget.setLayout(self.inside_vertical_mini_layout)
        self.inside_vertical_mini_layout.addLayout(self.vertical_mini_layout)

        # Butoane
        self.btn_plot = self.parent.create_button(self.update_plot, self.buttons_horizontal_layout_first_row, "Genereaza Piloni 3D")
        self.btn_clear = self.parent.create_button(self.clear_plot, self.buttons_horizontal_layout_first_row, "Șterge Graficul")
        self.create_roundFigure = self.parent.create_button(self.parallelipiped_figure_wrapper, self.buttons_horizontal_layout_first_row, "Gaura")
        self.create_parallelipipedFigure = self.parent.create_button(self.parallelipiped_figure_wrapper, self.buttons_horizontal_layout_first_row, "Paralelipiped")

        self.setLayout(self.main_grid_layout)

    
    def parallelipiped_figure_wrapper(self):
        # Creează o instanță nouă de createMiniFigure
        mini = createMiniFigure(
            plot_shapes_values_dictionary=self.plot_shapes_values_dictionary,
            input_boxes=self.input_boxes,
            parent_layout=self.vertical_mini_layout,
            parent=self.parent
        )
        
        # Creează paralelipipedul (acesta va actualiza plot-ul)
        mini.create_miniFigure_parallelipiped()

        # Păstrează instanța în listă pentru a o gestiona mai ușor
        self.mini_instances.append(mini)
        #self.plot_drill_parallelepiped()

    def init_plot(self):
        self.plot_manager = PlotManager(self.plot_container_widget)
        self.plot_drillplate((0.5, 0.5, 0.5, 1), 0, 30, 0, 20, 0, 2.5)
        self.plot_drill_parallelepiped((0, 3, 1, 0.4), 1, 10, 1, 7, 0, 2.5)    
        #self.create_drill_surface_plot((0, 2, 3, 0.4), 1, 10, 1, 7, 0, 2.5)

        self.plot_manager.plot_cylinder(x_center=15, y_center=15, z_min=0, height=2.6, radius=2, color=(1, 0, 0, 0.8))

        self.update_plot()

    def plot_drill_parallelepiped(self, color_rgba, x_min, x_max, y_min, y_max, z_min, z_max):
        id = len(self.plot_shapes_values_dictionary)
        key = f"{id}_drillparallelipiped_topMask"

        self.plot_shapes_values_dictionary[key] = (color_rgba, x_min, x_max, y_min, y_max, z_min - 0.01, z_max + 0.01)

        key = f"{id}_drillparallelipiped_bottomMask"
        self.plot_shapes_values_dictionary[key] = (color_rgba, x_min, x_max, y_min, y_max, z_min + 0.01, z_max - 0.01)

        #self.check_for_z_fighting()

    def plot_drillplate(self, color_rgba, x_min, x_max, y_min, y_max, z_min, z_max):
        id = len(self.plot_shapes_values_dictionary)
        key = f"{id}_drillplate"

        self.plot_shapes_values_dictionary[key] = (color_rgba, x_min, x_max, y_min, y_max, z_min, z_max)

    def check_for_z_fighting(self):
        offset = 0.09

        for key, (color, x_min, x_max, y_min, y_max, z_min, z_max) in self.plot_shapes_values_dictionary.items():
            adjusted_z_min = z_min + offset
            adjusted_z_max = z_max - offset
            self.plot_shapes_values_dictionary[key] = (color, x_min, x_max, y_min, y_max, adjusted_z_min, adjusted_z_max)

    def remove_drill_surface(self, key):
        if key in self.plot_shapes_values_dictionary:
            del self.plot_shapes_values_dictionary[key]

    def clear_plot(self):
        self.plot_manager.clear()

    def update_plot(self):
        self.plot_manager.clear()
        self.plot_manager.plot_cylinder(x_center=15, y_center=15, z_min=0, height=2.5, radius=2, color=(1, 0, 0, 0.8))

        for val in self.plot_shapes_values_dictionary.values():
            color, x_min, x_max, y_min, y_max, z_min, z_max = val
            self.plot_manager.plot_box(x_min, x_max, y_min, y_max, z_min, z_max, color=color)