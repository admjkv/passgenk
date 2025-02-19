import sys
import string
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QCheckBox
)

class PassGenk(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PassGenk - Password Generator")
        self.setFixedSize(300, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Password length selection
        length_layout = QHBoxLayout()
        length_label = QLabel("Password Length:")
        self.length_spin = QSpinBox()
        self.length_spin.setRange(6, 32)
        self.length_spin.setValue(12)
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_spin)
        layout.addLayout(length_layout)

        # Options for character types
        self.include_uppercase = QCheckBox("Include Uppercase")
        self.include_uppercase.setChecked(True)
        self.include_digits = QCheckBox("Include Digits")
        self.include_digits.setChecked(True)
        self.include_symbols = QCheckBox("Include Symbols")
        layout.addWidget(self.include_uppercase)
        layout.addWidget(self.include_digits)
        layout.addWidget(self.include_symbols)

        # Display for generated password
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        layout.addWidget(self.password_display)

        # Generate password button
        generate_button = QPushButton("Generate Password")
        generate_button.clicked.connect(self.generate_password)
        layout.addWidget(generate_button)

        # Copy to clipboard button
        copy_button = QPushButton("Copy to Clipboard");
        copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(copy_button)

        self.setLayout(layout)

    def generate_password(self):
        length = self.length_spin.value()
        
        # Always include lowercase letters as a base
        chars = string.ascii_lowercase
        if self.include_uppercase.isChecked():
            chars += string.ascii_uppercase
        if self.include_digits.isChecked():
            chars += string.digits
        if self.include_symbols.isChecked():
            chars += string.punctuation

        if not chars:
            self.password_display.setText("No characters selected")
            return

        password = "".join(random.choice(chars) for _ in range(length))
        self.password_display.setText(password)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_display.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PassGenk()
    window.show()
    sys.exit(app.exec())
