import serial
import serial.tools.list_ports


class serialConnectionBackend():
    def __init__(self, parent, threadRefference):
        self.threadRefference = threadRefference
        self.parent = parent
        self.ser = None
        self.reader = None

    def find_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def send_data(self, data):
        if self.ser.is_open and data is not None:
            self.ser.write((data.strip() + '\n').encode('utf-8'))
            self.ser.flush()
            response = self.ser.readline().decode().strip()
            return response

    def read_data(self):
        if self.ser.in_waiting > 0:
            data = self.ser.readline().decode('utf-8').rstrip()
            print("Arduino:", data)
            return data
        return None
    
    def connect_to_port(self):    
        port = self.parent.serialConnectionFrontend.return_target_port()
        
        if not port:  # Ensure the port is valid
            print("Error: No port selected.")
            return

        try:
            self.ser = serial.Serial(port, 115200, timeout=1)
            self.ser.flush()
            print(f"Connected to {port}")
        except serial.SerialException as e:
            print(f"Failed to connect: {e}")  
     
    def thread_read_data(self):
        if self.ser is None or not self.ser.is_open:
            print("Serial port not connected.")
            return

        self.reader = self.threadRefference(self.ser)
        self.reader.data_received.connect(self.handle_data)
        self.reader.start()

    def handle_data(self, data):
        print("Arduino:", data)

    def stop_reading(self, event=None):
        if self.reader:
            self.reader.stop()
            self.reader = None
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.ser = None
        if event:
            event.accept()

