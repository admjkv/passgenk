import sys
import string
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QCheckBox
)
from PyQt6.QtCore import QTimer

class PassGenk(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PassGenk - Password Generator")
        self.setFixedSize(300, 300)
        self.initUI()
        self.generate_password()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel("PassGenk")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)
        
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

        self.include_uppercase.stateChanged.connect(self.generate_password)
        self.include_digits.stateChanged.connect(self.generate_password)
        self.include_symbols.stateChanged.connect(self.generate_password)
        self.length_spin.valueChanged.connect(self.generate_password)

        # Password strength indicator
        strength_layout = QHBoxLayout()
        strength_label = QLabel("Password Strength:")
        self.strength_display = QLabel("N/A")
        strength_layout.addWidget(strength_label)
        strength_layout.addWidget(self.strength_display)
        layout.addLayout(strength_layout)

        # Display for generated password
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        layout.addWidget(self.password_display)

        # Generate password button
        generate_button = QPushButton("Generate Password")
        generate_button.clicked.connect(self.generate_password)
        layout.addWidget(generate_button)

        # Copy to clipboard button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

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
        self.calculate_password_strength(password)

    def calculate_password_strength(self, password):
        # Simple password strength calculation
        strength = 0
        
        # Length contribution
        if len(password) >= 8:
            strength += 1
        if len(password) >= 12:
            strength += 1
        if len(password) >= 16:
            strength += 1
            
        # Character variety contribution
        if any(c.islower() for c in password):
            strength += 1
        if any(c.isupper() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c in string.punctuation for c in password):
            strength += 1
        
        # Set strength level and color
        if strength <= 2:
            self.strength_display.setText("Weak")
            self.strength_display.setStyleSheet("color: red;")
        elif strength <= 4:
            self.strength_display.setText("Medium")
            self.strength_display.setStyleSheet("color: orange;")
        elif strength <= 6:
            self.strength_display.setText("Strong")
            self.strength_display.setStyleSheet("color: green;")
        else:
            self.strength_display.setText("Very Strong")
            self.strength_display.setStyleSheet("color: darkgreen;")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        password = self.password_display.text()
        if password and password != "No characters selected":
            clipboard.setText(password)
            
            # Save original text
            original_text = self.copy_button.text()
            
            # Show feedback
            self.copy_button.setText("Copied!")
            
            # Restore original text after a short delay
            QTimer.singleShot(1000, lambda: self.copy_button.setText(original_text))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PassGenk()
    window.show()
    sys.exit(app.exec())
