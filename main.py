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
        # Strength calculation
        strength = 0
        
        # Length contribution
        length = len(password)
        if length >= 8:
            strength += 1
        if length >= 12:
            strength += 1
        if length >= 16:
            strength += 1
        if length >= 20:
            strength += 1
        
        # Character variety contribution
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)
        
        variety_count = sum([has_lower, has_upper, has_digit, has_symbol])
        strength += variety_count
        
        # Check for character distribution
        char_counts = {}
        for c in password:
            if c in char_counts:
                char_counts[c] += 1
            else:
                char_counts[c] = 1
        
        # Reward for having unique characters (higher entropy)
        unique_ratio = len(char_counts) / length
        if unique_ratio > 0.7:
            strength += 1
        
        # Check for common patterns
        consecutive_count = 0
        previous_char = None
        has_sequence = False
        
        for c in password:
            if previous_char:
                if ord(c) == ord(previous_char) + 1:
                    consecutive_count += 1
                    if consecutive_count >= 3:
                        has_sequence = True
                        break
                else:
                    consecutive_count = 0
            previous_char = c
            
        if has_sequence:
            strength -= 1
            
        # Penalize repeated characters
        repeats = any(count > length * 0.3 for count in char_counts.values())
        if repeats:
            strength -= 1
        
        # Set strength level and color
        if strength <= 3:
            self.strength_display.setText("Weak")
            self.strength_display.setStyleSheet("color: red; font-weight: bold;")
        elif strength <= 5:
            self.strength_display.setText("Medium")
            self.strength_display.setStyleSheet("color: orange; font-weight: bold;")
        elif strength <= 7:
            self.strength_display.setText("Strong")
            self.strength_display.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.strength_display.setText("Very Strong")
            self.strength_display.setStyleSheet("color: darkgreen; font-weight: bold;")

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
