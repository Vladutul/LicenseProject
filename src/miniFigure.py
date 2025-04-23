from qtpy.QtWidgets import QWidget, QLineEdit, QGridLayout
import numpy as np
import pyqtgraph.opengl as gl


class createMiniFigure:
    def __init__(self, plot_shapes_values_dictionary, input_boxes, parent_layout, parent=None):
        self.plot_shapes_values_dictionary = plot_shapes_values_dictionary
        self.input_boxes = input_boxes
        self.parent_layout = parent_layout
        self.parent = parent

        self.view_miniFigure = gl.GLViewWidget()
        self.view_miniFigure.setCameraPosition(distance=20)
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

    def create_miniFigure_parallelipiped(self):
        id = len(self.plot_shapes_values_dictionary)
        key = f"id_{id}"

        x1, x2, y1, y2, z1, z2 = 1, 10, 1, 7, 0, 2.5
        color = (0, 3, 1, 0.4)

        self.plot_shapes_values_dictionary[key] = {
            'real_values': (x1, x2, y1, y2, z1, z2, color),
            'top_mask': None,
            'bottom_mask': None
        }

        self.plot_box_miniFigure(x1, x2, y1, y2, z1, z2, color)
        self.input_boxes[key] = {}

        mini_grid_layout = QGridLayout()
        mini_widget = QWidget()
        mini_widget.setLayout(mini_grid_layout)
        mini_widget.setFixedSize(300, 250)

        labels = ['x1', 'x2', 'y1', 'y2', 'z1', 'z2']
        default_values = [x1, x2, y1, y2, z1, z2]

        edit_button = self.parent.create_button(
            lambda k=key: self.edit_shape_values_parallelipiped(key), mini_grid_layout, "Edit", 0, 0)
        remove_button = self.parent.create_button(
            lambda k=key, w=mini_widget: self.remove_shape(k, w), mini_grid_layout, "Remove", 1, 0)

        edit_button.setFixedSize(50, 25)
        remove_button.setFixedSize(50, 25)

        for i, (label, value) in enumerate(zip(labels, default_values), start=2):
            line_edit = QLineEdit(str(value))
            line_edit.setFixedWidth(50)
            self.input_boxes[key][label] = line_edit
            mini_grid_layout.addWidget(line_edit, i, 0)
            line_edit.editingFinished.connect(lambda l=label, k=key: self.edit_shape_values_parallelipiped(k))

        mini_grid_layout.addWidget(self.view_miniFigure, 0, 1, 8, 1)
        self.parent_layout.addWidget(mini_widget)
    
    def edit_shape_values_parallelipiped(self, key, miniFigure = None):
        try:
            boxes = self.input_boxes[key]

            x1 = float(boxes['x1'].text())
            x2 = float(boxes['x2'].text())
            y1 = float(boxes['y1'].text())
            y2 = float(boxes['y2'].text())
            z1 = float(boxes['z1'].text())
            z2 = float(boxes['z2'].text())

            color = self.plot_shapes_values_dictionary[key]['real_values'][-1]  # Retain the original color

            self.plot_shapes_values_dictionary[key]['real_values'] = (x1, x2, y1, y2, z1, z2, color)
            #miniFigure.plot_box_miniFigure(x1, x2, y1, y2, z1, z2, color)

        except ValueError:
            print("Invalid input: please enter valid numbers.")

    def remove_shape(self, key, widget):
        if key in self.plot_shapes_values_dictionary:
            del self.plot_shapes_values_dictionary[key]
        if key in self.input_boxes:
            del self.input_boxes[key]
        widget.setParent(None)  # Șterge widget-ul din interfață

    def create_shape_round(self):
        pass
    def edit_existing_shape_round(self):
        pass