import json

class SaveAndLoadProjectClass:
    def __init__(self, plot_shapes_values_dictionary_reference):
        self.plot_shapes_values_dictionary_reference = plot_shapes_values_dictionary_reference

    def open_project(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.plot_shapes_values_dictionary_reference.update(data)

    def save_project(self, filepath):
        with open(filepath, 'w') as file:
            json.dump(self.plot_shapes_values_dictionary_reference, file, indent=4)

