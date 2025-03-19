import sys
import string
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QCheckBox
)
from PyQt6.QtCore import QTimer
from collections import Counter

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
        self.exclude_similar = QCheckBox("Exclude Similar Characters (1, l, I, 0, O)")
        layout.addWidget(self.include_uppercase)
        layout.addWidget(self.include_digits)
        layout.addWidget(self.include_symbols)
        layout.addWidget(self.exclude_similar)

        self.include_uppercase.stateChanged.connect(self.generate_password)
        self.include_digits.stateChanged.connect(self.generate_password)
        self.include_symbols.stateChanged.connect(self.generate_password)
        self.exclude_similar.stateChanged.connect(self.generate_password)
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
        
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase if self.include_uppercase.isChecked() else ""
        digits = string.digits if self.include_digits.isChecked() else ""
        symbols = string.punctuation if self.include_symbols.isChecked() else ""
        
        # Remove similar characters if needed
        if self.exclude_similar.isChecked():
            similar_chars = set('Il1O0o')
            lowercase = ''.join(c for c in lowercase if c not in similar_chars)
            uppercase = ''.join(c for c in uppercase if c not in similar_chars)
            digits = ''.join(c for c in digits if c not in similar_chars)
            symbols = ''.join(c for c in symbols if c not in similar_chars)
        
        # Combine all allowed character sets
        all_chars = lowercase + uppercase + digits + symbols
        
        if not all_chars:
            self.password_display.setText("No characters selected")
            return
        
        # Ensure we have at least one character from each selected category
        required_chars = []
        if lowercase:
            required_chars.append(random.choice(lowercase))
        if uppercase:
            required_chars.append(random.choice(uppercase))
        if digits:
            required_chars.append(random.choice(digits))
        if symbols:
            required_chars.append(random.choice(symbols))
        
        # Fill the rest with random characters
        remaining_length = max(0, length - len(required_chars))
        password_chars = required_chars + [random.choice(all_chars) for _ in range(remaining_length)]
        
        # Shuffle to avoid predictable positions
        random.shuffle(password_chars)
        password = ''.join(password_chars)
        
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
        char_counts = Counter(password)
        
        # Reward for having unique characters (higher entropy)
        unique_ratio = len(char_counts) / length
        if unique_ratio > 0.7:
            strength += 1
        
        # Check for common patterns
        if has_sequence(password):
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

def has_sequence(password, min_length=3):
    for i in range(len(password) - min_length + 1):
        is_sequence = True
        for j in range(i + 1, i + min_length):
            if ord(password[j]) != ord(password[j-1]) + 1:
                is_sequence = False
                break
        if is_sequence:
            return True
    return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PassGenk()
    window.show()
    sys.exit(app.exec())
