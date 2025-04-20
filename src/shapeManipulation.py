from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
import pyqtgraph.opengl as gl
import numpy as np


class shapeManipulationClass(QWidget):
    def __init__(self, parent, container):
        super(shapeManipulationClass, self).__init__(container)
        self.axis_end_points = {}
        self.drill_diameter = 0
        self.parent = parent


        self.init_UI()
        self.init_plot()

    def test_function(self):
        print("test code again")
        pass
    
    def test_function(self):
        print("test code again")
        pass

    def test_function(self):
        print("test code again")
        pass
    
    def init_UI(self):
        self.main_grid_layout = QGridLayout()
        self.buttons_horizontal_layout_first_row = QHBoxLayout()

        self.plot_container_widget = QWidget()
        self.plot_container_layout = QGridLayout()

        self.left_vertical_miniFigures_layout = QWidget()
        self.inside_left_vertical_miniFigures_layout = QGridLayout()

        self.parent.add_to_layout(self.buttons_horizontal_layout_first_row, self.main_grid_layout, 0,0,1,9)

        self.plot_container_widget.setLayout(self.plot_container_layout)
        self.parent.add_to_layout(self.plot_container_widget, self.main_grid_layout, 2,2,7,7)

        self.left_vertical_miniFigures_layout.setLayout(self.inside_left_vertical_miniFigures_layout)
        self.parent.add_to_layout(self.left_vertical_miniFigures_layout, self.main_grid_layout, 2,0,7,2)


        self.btn_plot = self.parent.create_button(self.update_plot, self.buttons_horizontal_layout_first_row,"Genereaza Piloni 3D")
        self.btn_clear = self.parent.create_button(self.clear_plot, self.buttons_horizontal_layout_first_row,"Șterge Graficul")

        self.create_roundFigure = self.parent.create_button(self.create_miniFigure_round, self.buttons_horizontal_layout_first_row, "Gaura")
        self.create_parallelipipedFigure = self.parent.create_button(self.create_miniFigure_parallelipiped, self.buttons_horizontal_layout_first_row, "Paralelipiped")


        self.setLayout(self.main_grid_layout)

    def create_miniFigure_round(self):
        miniFigure = createMiniFigure(self.left_vertical_miniFigures_layout)

        return miniFigure
    
    def create_miniFigure_parallelipiped(self):
        miniFigure = createMiniFigure(self.left_vertical_miniFigures_layout)
        miniFigure.plot_box_miniFigure(1, 10, 1, 7, 0, 2.5, (0, 3, 1, 0.4))
        return miniFigure 
        pass

    def init_plot(self):
        self.plot_manager = PlotManager(self.plot_container_widget)
        self.plot_drillplate((0.5, 0.5, 0.5, 1), 0, 30, 0, 20, 0, 2.5)
        self.plot_drill_parallelepiped((0, 3, 1, 0.4), 1, 10, 1, 7, 0, 2.5)    
        #self.create_drill_surface_plot((0, 2, 3, 0.4), 1, 10, 1, 7, 0, 2.5)

        print(self.axis_end_points)
        self.plot_manager.plot_cylinder(x_center=15, y_center=15, z_min=0, height=2.6, radius=2, color=(1, 0, 0, 0.8))

        self.update_plot()

    def plot_drill_parallelepiped(self, color_rgba, x_min, x_max, y_min, y_max, z_min, z_max):
        id = len(self.axis_end_points)
        key = f"{id}_drillparallelipiped_topMask"

        self.axis_end_points[key] = (color_rgba, x_min, x_max, y_min, y_max, z_min - 0.01, z_max + 0.01)

        key = f"{id}_drillparallelipiped_bottomMask"
        self.axis_end_points[key] = (color_rgba, x_min, x_max, y_min, y_max, z_min + 0.01, z_max - 0.01)

        #self.check_for_z_fighting()

    def plot_drillplate(self, color_rgba, x_min, x_max, y_min, y_max, z_min, z_max):
        id = len(self.axis_end_points)
        key = f"{id}_drillplate"

        self.axis_end_points[key] = (color_rgba, x_min, x_max, y_min, y_max, z_min, z_max)

    def check_for_z_fighting(self):
        offset = 0.09

        for key, (color, x_min, x_max, y_min, y_max, z_min, z_max) in self.axis_end_points.items():
            adjusted_z_min = z_min + offset
            adjusted_z_max = z_max - offset
            self.axis_end_points[key] = (color, x_min, x_max, y_min, y_max, adjusted_z_min, adjusted_z_max)

    def remove_drill_surface(self, key):
        if key in self.axis_end_points:
            del self.axis_end_points[key]

    def clear_plot(self):
        self.plot_manager.clear()

    def update_plot(self):
        self.plot_manager.clear()
        self.plot_manager.plot_cylinder(x_center=15, y_center=15, z_min=0, height=2.5, radius=2, color=(1, 0, 0, 0.8))

        for val in self.axis_end_points.values():
            color, x_min, x_max, y_min, y_max, z_min, z_max = val
            self.plot_manager.plot_box(x_min, x_max, y_min, y_max, z_min, z_max, color=color)


class createMiniFigure:
    def __init__(self, container):
        self.view_miniFigure = gl.GLViewWidget()
        self.view_miniFigure.setCameraPosition(distance=20)
        container.layout().addWidget(self.view_miniFigure)
        self.items_miniFigure = []

    def plot_box_miniFigure(self, x_min, x_max, y_min, y_max, z_min, z_max, color=(0.5, 0.5, 1, 0.5)):
        verts = np.array([
            [x_min, y_min, z_min],
            [x_max, y_min, z_min],
            [x_max, y_max, z_min],
            [x_min, y_max, z_min],
            [x_min, y_min, z_max],
            [x_max, y_min, z_max],
            [x_max, y_max, z_max],
            [x_min, y_max, z_max]
        ])

        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # bottom
            [4, 5, 6], [4, 6, 7],  # top
            [0, 1, 5], [0, 5, 4],  # front
            [2, 3, 7], [2, 7, 6],  # back
            [1, 2, 6], [1, 6, 5],  # right
            [3, 0, 4], [3, 4, 7],  # left
        ])

        mesh = gl.GLMeshItem(vertexes=verts, faces=faces,
                             faceColors=np.array([color] * len(faces)),
                             smooth=False, drawEdges=True, edgeColor=(0, 0, 0, 1))
        self.view_miniFigure.addItem(mesh)
        self.items_miniFigure.append(mesh)


    def create_shape(self, object):

        pass
    
    def create_shape_round(self):
        pass

    def create_shape_parallelipiped(self):
        pass
    
    '''def edit_existing_shape(self, object):
        if shape of object is round:
            pass
        elif shape of object is parallelipiped:
            pass
        else:
            pass

        pass'''
    
    def edit_existing_shape_round(self):
        pass

    def edit_existing_shape_parallelipiped(self):
        pass


class PlotManager:
    def __init__(self, container):
        self.view = gl.GLViewWidget()
        self.view.setCameraPosition(distance=100)
        container.layout().addWidget(self.view)

        grid = gl.GLGridItem()
        grid.setSize(100, 100)
        grid.setSpacing(5, 5)
        self.view.addItem(grid)

        self.items = []

    def plot_box(self, x_min, x_max, y_min, y_max, z_min, z_max, color=(0.5, 0.5, 1, 0.5)):
        verts = np.array([
            [x_min, y_min, z_min],
            [x_max, y_min, z_min],
            [x_max, y_max, z_min],
            [x_min, y_max, z_min],
            [x_min, y_min, z_max],
            [x_max, y_min, z_max],
            [x_max, y_max, z_max],
            [x_min, y_max, z_max]
        ])

        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # bottom
            [4, 5, 6], [4, 6, 7],  # top
            [0, 1, 5], [0, 5, 4],  # front
            [2, 3, 7], [2, 7, 6],  # back
            [1, 2, 6], [1, 6, 5],  # right
            [3, 0, 4], [3, 4, 7],  # left
        ])

        mesh = gl.GLMeshItem(vertexes=verts, faces=faces,
                             faceColors=np.array([color] * len(faces)),
                             smooth=False, drawEdges=True, edgeColor=(0, 0, 0, 1))
        self.view.addItem(mesh)
        self.items.append(mesh)

    def plot_cylinder(self, x_center, y_center, z_min, height, radius=1.0, resolution=32, color=(1, 0, 0, 1)):
        offset = 0.2
        height = height + offset
        theta = np.linspace(0, 2 * np.pi, resolution)
        x_circle = radius * np.cos(theta)
        y_circle = radius * np.sin(theta)

        bottom = np.vstack((x_circle + x_center, y_circle + y_center, np.full_like(theta, z_min))).T

        top = np.vstack((x_circle + x_center, y_circle + y_center, np.full_like(theta, z_min + height))).T

        vertices = np.vstack((bottom, top))
        center_bottom = [x_center, y_center, z_min]
        center_top = [x_center, y_center, z_min + height]
        vertices = np.vstack((vertices, center_bottom, center_top))

        faces = []
        for i in range(resolution):
            next_i = (i + 1) % resolution
            faces.append([i, next_i, resolution + next_i])  # laturi
            faces.append([i, resolution + next_i, resolution + i])  # laturi

        for i in range(resolution):
            next_i = (i + 1) % resolution
            faces.append([i, next_i, 2 * resolution])  # Fața de jos

        for i in range(resolution):
            next_i = (i + 1) % resolution
            faces.append([i + resolution, next_i + resolution, 2 * resolution + 1])  # Fața de sus

        faces = np.array(faces)

        mesh = gl.GLMeshItem(vertexes=vertices, faces=faces,
                            faceColors=np.array([color] * len(faces)),
                            smooth=False, drawEdges=True, edgeColor=(0, 0, 0, 1))
        mesh.setGLOptions('translucent')
        self.view.addItem(mesh)
        self.items.append(mesh)

    def clear(self):
        for item in self.items:
            self.view.removeItem(item)
        self.items.clear()
