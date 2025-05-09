import serial
import serial.tools.list_ports
import time
import os


class serialConnectionBackend():
    def __init__(self, parent, threadRefference):
        self.threadRefference = threadRefference
        self.parent = parent
        self.ser = None
        self.reader = None
        self.filepath = "C:/Users/Vladutul/Documents/FisierTestgCodeLicenta/output.gcode"


    def send_gcode_file(self, wait_for='ok', delay=0.1):
        if not os.path.isfile(self.filepath):
            print(f"File not found: {self.filepath}")
            return

        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='replace') as file:
                for line_number, line in enumerate(file, 1):
                    # Strip comments and whitespace
                    line = line.split(';', 1)[0].strip()
                    if not line:
                        continue
                    try:
                        # Send the line as a string
                        response = self.send_data(str(line))
                        print(f"Line {line_number}: Sent: {line} | Received: {response}")

                        while not (isinstance(response, str) and wait_for in response.lower()):
                            time.sleep(delay)
                            response = self.ser.readline().decode(errors='ignore').strip()
                            if response:
                                print(f"Line {line_number}: Waiting... Received: {response}")

                        time.sleep(delay)
                    except Exception as e:
                        print(f"Error sending line {line_number}: {e}")
                        break
        except Exception as e:
            print(f"Error opening or reading file: {e}")

    def send_data(self, data):
        print(data)
        if self.ser.is_open and data is not None:
            self.ser.write((data.strip() + '\n').encode('utf-8'))
            self.ser.flush()
            response = self.ser.readline().decode().strip()
            return response
        
    def find_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
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

