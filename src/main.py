import sys
from PyQt5.QtWidgets import QApplication
from classMain import classUIinitialization


def main():
    app = QApplication(sys.argv)
    window = classUIinitialization()
    window.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()