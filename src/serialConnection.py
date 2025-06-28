from serialConnectionBackend import serialConnectionBackend
from serialConnectionFrontend import serialConnectionFrontend
from serialThread import serialReadThreadClass

class serialConnectionClass():
    def __init__(self, main_reference, container):

        self.serialConnectionFrontend = serialConnectionFrontend(self, main_reference, container)    
        self.serialConnectionBackend = serialConnectionBackend(self, serialReadThreadClass)
        
    def find_ports(self):
        return self.serialConnectionBackend.find_ports()