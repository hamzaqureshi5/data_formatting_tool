import sys
import re
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog,QComboBox,QStyledItemDelegate
from PyQt6.QtGui import QIcon,QIntValidator

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel

class CenterAlignedItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter
        super().paint(painter, option, index)



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DATA FORMATING TOOL")
        self.setGeometry(100, 100, 300, 200)
        self.setFixedHeight(400)
        self.setFixedWidth(500)
        self.setWindowIcon(QIcon("ico.ico"))
        
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label1 = QLabel("INPUT FILE PATH:", self)
        self.layout.addWidget(self.label1)

        self.edit1 = QLineEdit(self)
        self.edit1.setReadOnly(True)
        self.layout.addWidget(self.edit1)

        self.browse_button = QPushButton("BROWSE", self)
        self.browse_button.clicked.connect(self.browseFile)
        self.layout.addWidget(self.browse_button)

        self.sym_label = QLabel("SELECT SYMBOL:", self)
        self.layout.addWidget(self.sym_label)

        self.sym_edit = QComboBox(self)
        
        list_sym=["SPACE","COMMA","DOT"]
        self.sym_edit.addItems(list_sym)
        self.sym_edit.setCurrentText(list_sym[0])
        self.sym_edit.setItemDelegate(CenterAlignedItemDelegate())

        self.layout.addWidget(self.sym_edit)
       
#        self.layout.addWidget(self.sym_edit)

        self.label2 = QLabel("SYMBOL AFTER CHARACTERS:", self)
        self.layout.addWidget(self.label2)

        self.edit2 = QLineEdit(self)
        int_validator = QIntValidator()
        self.edit2.setValidator(int_validator)
        self.edit2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.edit2)

        self.submit_button = QPushButton("SUBMIT", self)
        self.submit_button.clicked.connect(self.generateResults)
        self.layout.addWidget(self.submit_button)

        self.text_box = QTextEdit(self)
        self.layout.addWidget(self.text_box)
        
        url = "https://github.com/hamza7771"

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.developer_label = QLabel("Developed by : HAMZA QURESHI", self)
        self.developer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align center
        self.layout.addWidget(self.developer_label)

        self.version_label = QLabel("Version 3.0.0 | Programming Language used : Python", self)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align center
        self.layout.addWidget(self.version_label)

        self.git_label = QLabel(self)   
        self.git_label.setText("Visit for more: "+f'<a href="{url}">{url}</a>')
        self.git_label.setOpenExternalLinks(True)
        self.git_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align center

        self.layout.addWidget(self.git_label)

    def browseFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            self.edit1.setText(file_path)
            self.inputfile=file_path

    def Get_symbol(self,symbol):
        if symbol == "SPACE":
            symbol_ret=" "
        elif symbol =="COMMA":
            symbol_ret=","
        elif symbol =="DOT":
            symbol_ret="."
        else:
            symbol_ret=""
        return symbol_ret

    def generateResults(self):
        file_path = self.edit1.text()
        input_variable = self.edit2.text()
        symbol=self.Get_symbol(self.sym_edit.currentText())

        if file_path and input_variable and symbol:            
            result = f"File: {file_path}, \nExpect space after every {input_variable} character/characters\nOutput file generated named as \"Output.txt\""
            self.text_box.setPlainText(result)
            self.submit(file_path,int(input_variable),symbol)
        else:
            self.text_box.setPlainText("Please enter a valid file path and input variable.")



    def process_and_generate(self,input_file_path, output_file_path, symbol_after_x,symbol:str):
        try:
            with open(input_file_path, "r") as input_file:
                content = input_file.read()

            content_without_spaces = re.sub(r"\s+", "", content)

            processed_content = symbol.join(content_without_spaces[i:i+symbol_after_x] for i in range(0, len(content_without_spaces), symbol_after_x))

            with open(output_file_path, "w") as output_file:
                output_file.write(processed_content)

            return True  # Successfully processed and generated the output file

        except Exception as e:
            self.text_box.append(str(e))
            return False  # Failed to process and generate the output file

    def submit(self,input_path,spaces_after,symbol):
        output_path = "output.txt"

        if self.process_and_generate(input_path, output_path, spaces_after,symbol):
            self.text_box.append(str("Processing and generation completed successfully."))

        else:
            self.text_box.append(str("Processing and generation failed."))
            

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()