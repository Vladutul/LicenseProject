import pyqtgraph.opengl as gl
import numpy as np


class PlotManager:
    def __init__(self, container, plot_shapes_values_dictionary):
        self.view = gl.GLViewWidget()
        self.view.setCameraPosition(distance=100)
        container.layout().addWidget(self.view)

        grid = gl.GLGridItem()
        grid.setSize(7000, 7000)
        grid.setSpacing(5, 5)
        self.view.addItem(grid)

        self.plot_shapes_values_dictionary = plot_shapes_values_dictionary
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

    def plot_cylinder(self, x_center, y_center, z_min, height, radius=1.0, color=(1, 0, 0, 1)):
        resolution = 32
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

    def check_if_in_drillplate(self, x, y, z):
        x_min, x_max, y_min, y_max, z_min, z_max = self.plot_shapes_values_dictionary['drillplate']['real_values']
        return x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max

    def update_plot(self):
        self.clear_plot()

        def plot_mask_parallelipiped(x_min, x_max, y_min, y_max, z_min, z_max, color):
            self.plot_box(x_min, x_max, y_min, y_max, z_min, z_max, color=color)

        def plot_mask_cylinder(x_center, y_center, z_min, height, radius, color):
            self.plot_cylinder(x_center, y_center, z_min, height, radius, color=color)

        for key, val in self.plot_shapes_values_dictionary.items():
            shape_type = val.get('shape')
            real_values = val.get('real_values')

            if shape_type == 'parallelipiped':
                x_min, x_max, y_min, y_max, z_min, z_max, color = real_values
                self.plot_box(x_min, x_max, y_min, y_max, z_min, z_max, color)
                top_mask = val.get('top_mask')
                bottom_mask = val.get('bottom_mask')

                if top_mask:
                    x_min, x_max, y_min, y_max, z_min, z_max = top_mask
                    plot_mask_parallelipiped(x_min, x_max, y_min, y_max, z_min, z_max, color)

                if bottom_mask:
                    x_min, x_max, y_min, y_max, z_min, z_max = bottom_mask
                    plot_mask_parallelipiped(x_min, x_max, y_min, y_max, z_min, z_max, color)

            elif shape_type == 'roundHole':
                x_center, y_center, z_min, height, radius, color = real_values
                self.plot_cylinder(x_center, y_center, z_min, height, radius, color)
                top_mask = val.get('top_mask')
                bottom_mask = val.get('bottom_mask')

                if top_mask:
                    x_center, y_center, z_min, height, radius, color = top_mask
                    plot_mask_cylinder(x_center, y_center, z_min, height, radius, color)
                
                if bottom_mask:
                    x_center, y_center, z_min, height, radius, color = bottom_mask
                    plot_mask_cylinder(x_center, y_center, z_min, height, radius, color)
            
            elif shape_type == 'drillPlate':
                x_min, x_max, y_min, y_max, z_min, z_max, color = real_values
                self.plot_box(x_min, x_max, y_min, y_max, z_min, z_max, color)

    def clear_plot(self):
        for item in self.items:
            self.view.removeItem(item)
        self.items.clear()

    def init_plot(self):
        self.plot_manager = PlotManager(self.plot_container_widget)
        self.plot_drillplate((0.5, 0.5, 0.5, 1), 0, 30, 0, 20, 0, 2.5)
        self.plot_drill_parallelepiped((0, 3, 1, 0.4), 1, 10, 1, 7, 0, 2.5)    
        #self.create_drill_surface_plot((0, 2, 3, 0.4), 1, 10, 1, 7, 0, 2.5)

        self.plot_manager.plot_cylinder(x_center=15, y_center=15, z_min=0, height=2.6, radius=2, color=(1, 0, 0, 0.8))

        self.update_plot()