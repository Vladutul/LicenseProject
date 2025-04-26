from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea, QPushButton
from plot import PlotManager
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

    def init_UI(self):
        self.main_grid_layout = QGridLayout()
        self.buttons_horizontal_layout_first_row = QHBoxLayout()

        self.plot_container_widget = QWidget()
        self.plot_container_layout = QGridLayout()

        self.left_vertical_mini_widget = QWidget()
        self.vertical_mini_layout = QVBoxLayout()
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
        self.create_roundFigure = self.parent.create_button(self.roundShape_figure_wrapper, self.buttons_horizontal_layout_first_row, "Gaura")
        self.create_parallelipipedFigure = self.parent.create_button(self.parallelipipedShape_figure_wrapper, self.buttons_horizontal_layout_first_row, "Paralelipiped")

        self.setLayout(self.main_grid_layout)
    
    def update_plot(self):
        self.plotManager = PlotManager(self.plot_container_widget)
        self.plotManager.update_plot()

    def clear_plot(self):
        self.plotManager = PlotManager(self.plot_container_widget)
        self.plotManager.clear_plot()

    def parallelipipedShape_figure_wrapper(self):
        mini = self.mini_create_wrapper()
        mini.create_miniFigure_parallelipiped()
        self.mini_instances.append(mini)

    def roundShape_figure_wrapper(self):
        mini = self.mini_create_wrapper()
        mini.create_miniFigure_roundHole()
        self.mini_instances.append(mini)

    def mini_create_wrapper(self):
        mini = createMiniFigure(
            plot_shapes_values_dictionary=self.plot_shapes_values_dictionary,
            input_boxes=self.input_boxes,
            parent_layout=self.vertical_mini_layout,
            classUIinitialization=self.parent,
            shapeManipulationRefference=self
        )

        return mini