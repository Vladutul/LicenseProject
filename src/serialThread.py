from PyQt5.QtCore import QThread, pyqtSignal
import time


class serialReadThreadClass(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self._running = True

    def run(self):
        try:
            time.sleep(2)
            self.ser.flushInput()
            while self._running:
                if self.ser and self.ser.is_open:
                    if self.ser.in_waiting > 0:
                        try:
                            raw = self.ser.readline()
                            line = raw.decode('utf-8', errors='ignore').strip()
                            if line:
                                self.data_received.emit(line)
                        except Exception as e:
                            print(f"Serial read error: {e}")
                else:
                    break
        except Exception as e:
            print(f"Serial read error: {e}")


    def stop(self):
        self._running = False
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
        except:
            pass
        self.quit()
        self.wait()