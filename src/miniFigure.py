from qtpy.QtWidgets import QWidget, QLineEdit, QGridLayout
import numpy as np
import pyqtgraph.opengl as gl


class createMiniFigure:
    def __init__(self, plot_shapes_values_dictionary, input_boxes, parent_layout, classUIinitialization, shapeManipulationRefference):
        self.plot_shapes_values_dictionary = plot_shapes_values_dictionary
        self.input_boxes = input_boxes
        self.parent_layout = parent_layout
        self.classUIinitialization = classUIinitialization
        self.shapeManipulationRefference = shapeManipulationRefference

        self.view_miniFigure = gl.GLViewWidget()
        self.view_miniFigure.setCameraPosition(distance=20)
        self.items_miniFigure = []

    def create_miniFigure_drillPlate(self):
        id = len(self.plot_shapes_values_dictionary)
        key = f"id_{id}"

        x_center, y_center, z_min, height, radius = self.generate_unused_real_values_roundHole()
        color = (1, 0, 0, 0.8)

        self.plot_shapes_values_dictionary[key] = {
            'shape': 'drillPlate',
            'real_values': (x_center, y_center, z_min, height, radius, color),
            'top_mask': None,
            'bottom_mask': None,
            'visibleState': False
        }

        self.plot_miniFigure_roundHole(x_center, y_center, z_min, height, radius, color)
        self.input_boxes[key] = {}

        mini_widget, mini_grid_layout = self.create_mini_widget_layout()

        labels = ['x_min', 'x_max', 'y_min', 'y_max', 'z_min', 'z_max']
        default_values = [x_center, y_center, z_min, height, radius]

        show_button = self.classUIinitialization.create_button(
            lambda k=key: self.change_visibleState(k), mini_grid_layout, "Show", 0, 0)
        remove_button = self.classUIinitialization.create_button(
            lambda k=key, w=mini_widget: self.remove_shape(k, w), mini_grid_layout, "Remove", 1, 0)

        show_button.setFixedSize(50, 25)
        remove_button.setFixedSize(50, 25)

        for i, (label, value) in enumerate(zip(labels, default_values), start=2):
            line_edit = QLineEdit(str(value))
            line_edit.setFixedWidth(50)
            self.input_boxes[key][label] = line_edit
            mini_grid_layout.addWidget(line_edit, i, 0)
            line_edit.editingFinished.connect(lambda l=label, k=key: self.edit_shapeValues_roundHole(k))

        mini_grid_layout.addWidget(self.view_miniFigure, 0, 1, 7, 1)
        self.parent_layout.addWidget(mini_widget)

    def create_mini_widget_layout(self):
        mini_grid_layout = QGridLayout()
        mini_widget = QWidget()
        mini_widget.setLayout(mini_grid_layout)
        mini_widget.setFixedSize(300, 250)
        return mini_widget, mini_grid_layout

    def create_shape_real_values(self, key, values, shape_type):
        if shape_type == 'parallelipiped' or shape_type == 'drillPlate':
            x_min, x_max, y_min, y_max, z_min, z_max, color = values
            self.plot_shapes_values_dictionary[key] = {
                'shape': shape_type,
                'real_values': (x_min, x_max, y_min, y_max, z_min, z_max, color),
                'top_mask': None,
                'bottom_mask': None,
                'visibleState': False
            }
        elif shape_type == 'roundHole':
            x_center, y_center, z_min, height, radius, color = values
            self.plot_shapes_values_dictionary[key] = {
                'shape': shape_type,
                'real_values': (x_center, y_center, z_min, height, radius, color),
                'top_mask': None,
                'bottom_mask': None,
                'visibleState': False
            }
        
        return self.plot_shapes_values_dictionary[key]

    def create_miniFigure_parallelipiped(self):
        id = len(self.plot_shapes_values_dictionary)
        key = f"id_{id}"

        values = self.generate_unused_real_values_parallelipiped()
        self.plot_shapes_values_dictionary[key] = self.create_shape_real_values(key, values, 'parallelipiped')
        self.plot_miniFigure_parallelipiped(*values[:-1], color=values[-1])
        self.input_boxes[key] = {}

        mini_widget, mini_grid_layout = self.create_mini_widget_layout()

        labels = ['x1', 'x2', 'y1', 'y2', 'z1', 'z2']
        default_values = [values[:-1]]

        show_button = self.classUIinitialization.create_button(
            lambda k=key: self.change_visibleState(k), mini_grid_layout, "Show", 0, 0)
        remove_button = self.classUIinitialization.create_button(
            lambda k=key, w=mini_widget: self.remove_shape(k, w), mini_grid_layout, "Remove", 1, 0)

        show_button.setFixedSize(50, 25)
        remove_button.setFixedSize(50, 25)

        for i, (label, value) in enumerate(zip(labels, default_values), start=2):
            line_edit = QLineEdit(str(value))
            line_edit.setFixedWidth(50)
            self.input_boxes[key][label] = line_edit
            mini_grid_layout.addWidget(line_edit, i, 0)
            line_edit.editingFinished.connect(lambda l=label, k=key: self.edit_shapeValues_parallelipiped(k))

        mini_grid_layout.addWidget(self.view_miniFigure, 0, 1, 8, 1)
        self.parent_layout.addWidget(mini_widget)

    def plot_miniFigure_parallelipiped(self, x_min, x_max, y_min, y_max, z_min, z_max, color=(0.5, 0.5, 1, 0.5)):
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

    def edit_shapeValues_parallelipiped(self, key):
        try:
            # Get the input boxes for the specified key
            if key not in self.input_boxes:
                print(f"No input boxes found for key: {key}")
                return

            boxes = self.input_boxes[key]

            # Read the updated values from the input boxes
            x1 = float(boxes['x1'].text())
            x2 = float(boxes['x2'].text())
            y1 = float(boxes['y1'].text())
            y2 = float(boxes['y2'].text())
            z1 = float(boxes['z1'].text())
            z2 = float(boxes['z2'].text())

            # Retain the original color from the dictionary
            color = self.plot_shapes_values_dictionary[key]['real_values'][-1]

            # Update the dictionary with the new values
            self.plot_shapes_values_dictionary[key]['real_values'] = (x1, x2, y1, y2, z1, z2, color)

            # Clean the plot
            self.clear_plot()

            # Redraw the plot with the updated values
            self.plot_miniFigure_parallelipiped(x1, x2, y1, y2, z1, z2, color)

        except ValueError:
            print("Invalid input: please enter valid numbers.")

    def create_miniFigure_roundHole(self):
        id = len(self.plot_shapes_values_dictionary)
        key = f"id_{id}"

        values = self.generate_unused_real_values_roundHole()
        self.plot_shapes_values_dictionary[key] = self.create_shape_real_values(key, values, 'roundHole')
        self.plot_miniFigure_roundHole(*values[:-1], color=values[-1])
        self.input_boxes[key] = {}

        mini_widget, mini_grid_layout = self.create_mini_widget_layout()

        labels = ['x_center', 'y_center', 'z_min', 'height', 'radius']
        default_values = [*values[:-1]]

        show_button = self.classUIinitialization.create_button(
            lambda k=key: self.change_visibleState(k), mini_grid_layout, "Edit", 0, 0)
        remove_button = self.classUIinitialization.create_button(
            lambda k=key, w=mini_widget: self.remove_shape(k, w), mini_grid_layout, "Remove", 1, 0)

        show_button.setFixedSize(50, 25)
        remove_button.setFixedSize(50, 25)

        for i, (label, value) in enumerate(zip(labels, default_values), start=2):
            line_edit = QLineEdit(str(value))
            line_edit.setFixedWidth(50)
            self.input_boxes[key][label] = line_edit
            mini_grid_layout.addWidget(line_edit, i, 0)
            line_edit.editingFinished.connect(lambda l=label, k=key: self.edit_shapeValues_roundHole(k))

        mini_grid_layout.addWidget(self.view_miniFigure, 0, 1, 7, 1)
        self.parent_layout.addWidget(mini_widget)

    def plot_miniFigure_roundHole(self, x_center, y_center, z_min, height, radius, color):
        resolution = 100
        offset = 0.2
        height += offset

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
            faces.append([i, next_i, resolution + next_i])  # Side faces
            faces.append([i, resolution + next_i, resolution + i])  # Side faces

        for i in range(resolution):
            next_i = (i + 1) % resolution
            faces.append([i, next_i, 2 * resolution])  # Bottom face

        for i in range(resolution):
            next_i = (i + 1) % resolution
            faces.append([i + resolution, next_i + resolution, 2 * resolution + 1])  # Top face

        faces = np.array(faces)

        mesh = gl.GLMeshItem(vertexes=vertices, faces=faces,
                            faceColors=np.array([color] * len(faces)),
                            smooth=False, drawEdges=True, edgeColor=(0, 0, 0, 1))
        mesh.setGLOptions('translucent')
        self.view_miniFigure.addItem(mesh)
        self.items_miniFigure.append(mesh)

    def edit_shapeValues_roundHole(self, key):
        try:
            boxes = self.input_boxes[key]

            x_center = float(boxes['x_center'].text())
            y_center = float(boxes['y_center'].text())
            z_min = float(boxes['z_min'].text())
            height = float(boxes['height'].text())
            radius = float(boxes['radius'].text())

            color = self.plot_shapes_values_dictionary[key]['real_values'][-1]  # Retain the original color

            self.plot_shapes_values_dictionary[key]['real_values'] = (x_center, y_center, z_min, height, radius, color)
            self.clear_plot()
            self.plot_miniFigure_roundHole(x_center, y_center, z_min, height, radius, color)

        except ValueError:
            print("Invalid input: please enter valid numbers.")

    def remove_shape(self, key, widget):
        if key in self.plot_shapes_values_dictionary:
            del self.plot_shapes_values_dictionary[key]
        if key in self.input_boxes:
            del self.input_boxes[key]
        widget.setParent(None)

    def create_masks_for_real_values(self, key):
        if self.plot_shapes_values_dictionary[key]['shape'] == 'parallelipiped':
            pass
        elif self.plot_shapes_values_dictionary[key]['shape'] == 'roundHole':
            pass
        elif self.plot_shapes_values_dictionary[key]['shape'] == 'drillPlate':
            pass

        real_values = self.plot_shapes_values_dictionary[key]['real_values']
        x_min, x_max, y_min, y_max, z_min, z_max, color = real_values

        top_mask = (x_min, x_max, y_min, y_max, z_min - 0.01, z_max + 0.01, color)
        bottom_mask = (x_min, x_max, y_min, y_max, z_min + 0.01, z_max - 0.01, color)

        self.plot_shapes_values_dictionary[key]['top_mask'] = top_mask
        self.plot_shapes_values_dictionary[key]['bottom_mask'] = bottom_mask

    def clear_plot(self):
        for item in self.items_miniFigure:
            self.view_miniFigure.removeItem(item)
        self.items_miniFigure.clear()

    def generate_unused_real_values_parallelipiped(self):
        color = (0, 3, 1, 0.4)
        existing_ranges = []
        for key, data in self.plot_shapes_values_dictionary.items():
            real_values = data.get('real_values', [])
            if len(real_values) >= 2:
                x_min, x_max = real_values[:2]
                existing_ranges.append((x_min, x_max))

        x_min, x_max = -10, -3
        while any(x_min <= existing_x_max and x_max >= existing_x_min for existing_x_min, existing_x_max in existing_ranges):
            x_min -= 6
            x_max -= 6

        y_min, y_max = 1, 7
        z_min, z_max = 0, 2.5

        return x_min, x_max, y_min, y_max, z_min, z_max, color

    def generate_unused_real_values_roundHole(self):
        color = (1, 0, 0, 0.8)
        existing_centers = []
        for key, data in self.plot_shapes_values_dictionary.items():
            if data.get('shape') == 'roundHole':
                real_values = data.get('real_values', [])
                if len(real_values) >= 2:
                    x_center, y_center = real_values[:2]
                    existing_centers.append((x_center, y_center))

        x_center, y_center = -3, 15
        while any(abs(x_center - existing_x) < 2 and abs(y_center - existing_y) < 2 for existing_x, existing_y in existing_centers):
            x_center -= 5

        z_min = 0
        height = 2.6
        radius = 2

        return x_center, y_center, z_min, height, radius, color

    def change_visibleState(self, key):
        if key in self.plot_shapes_values_dictionary:
            state = not self.plot_shapes_values_dictionary[key]['visibleState']
            self.plot_shapes_values_dictionary[key]['visibleState'] = state

        self.shapeManipulationRefference.update_plot()

    def check_for_z_fighting(self):
        offset = 0.09

        for key, (color, x_min, x_max, y_min, y_max, z_min, z_max) in self.plot_shapes_values_dictionary.items():
            adjusted_z_min = z_min + offset
            adjusted_z_max = z_max - offset
            self.plot_shapes_values_dictionary[key] = (color, x_min, x_max, y_min, y_max, adjusted_z_min, adjusted_z_max)