import pyqtgraph.opengl as gl
import numpy as np


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

    def update_plot(self):
        self.clear()
        self.plot_cylinder(x_center=15, y_center=15, z_min=0, height=2.5, radius=2, color=(1, 0, 0, 0.8))

        for val in self.plot_shapes_values_dictionary.values():
            color, x_min, x_max, y_min, y_max, z_min, z_max = val
            self.plot_box(x_min, x_max, y_min, y_max, z_min, z_max, color=color)

    def clear(self):
        for item in self.items:
            self.view.removeItem(item)
        self.items.clear()