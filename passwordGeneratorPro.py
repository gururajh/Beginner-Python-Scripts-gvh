import random
import string
import tkinter as tk
from tkinter import messagebox
import re

# -------------------------
# Mappings for mnemonic hints
# -------------------------
phonetic_map_upper = {
    letter: word for letter, word in zip(string.ascii_uppercase,
    ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel",
     "India", "Juliet", "Kilo", "Lima", "Mike", "November", "Oscar", "Papa",
     "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey",
     "X-ray", "Yankee", "Zulu"])
}

phonetic_map_lower = {
    letter.lower(): phonetic_map_upper[letter].lower()
    for letter in phonetic_map_upper
}

digit_map = {
    "0": "Zero", "1": "One", "2": "Two", "3": "Three", "4": "Four",
    "5": "Five", "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine"
}

symbol_map = {
    "@": "At", "#": "Hash", "$": "Dollar", "%": "Percent", "&": "Ampersand",
    "*": "Star", "!": "Exclaim", "?": "Question", ".": "Dot", ",": "Comma",
    "+": "Plus", "-": "Dash", "_": "Underscore", "=": "Equals", "^": "Caret",
    "~": "Tilde", "/": "Slash", "\\": "Backslash", "(": "OpenParen", ")": "CloseParen"
}

# Password storage file
PASSWORD_STORE_FILE = "saved_passwords.txt"

# -------------------------
# Password Generation
# -------------------------
def generate_password(length, use_digits, use_uppercase, use_lowercase, use_symbols):
    char_types = []
    if use_digits:
        char_types.append(string.digits)
    if use_uppercase:
        char_types.append(string.ascii_uppercase)
    if use_lowercase:
        char_types.append(string.ascii_lowercase)
    if use_symbols:
        char_types.append(string.punctuation)

    if not char_types:
        raise ValueError("At least one character type must be selected")

    # Ensure at least one character from each selected type
    password = [random.choice(chars) for chars in char_types]
    remaining_length = length - len(password)
    all_chars = ''.join(char_types)
    password += [random.choice(all_chars) for _ in range(remaining_length)]
    random.shuffle(password)
    return ''.join(password)

# -------------------------
# Mnemonic Hint Creation
# -------------------------
def generate_hint(password):
    hint_parts = []
    for ch in password:
        if ch in digit_map:
            hint_parts.append(digit_map[ch])
        elif ch in phonetic_map_upper:
            hint_parts.append(phonetic_map_upper[ch])
        elif ch in phonetic_map_lower:
            hint_parts.append(phonetic_map_lower[ch])
        elif ch in symbol_map:
            hint_parts.append(symbol_map[ch])
        else:
            hint_parts.append(f"[{ch}]")  # fallback
    return " ".join(hint_parts)

# -------------------------
# Save password to file
# -------------------------
def save_password(password, filename=PASSWORD_STORE_FILE):
    try:
        with open(filename, 'a') as f:
            f.write(password + '\n')
        return True
    except Exception as e:
        print(f"Error saving password: {e}")
        return False

# -------------------------
# Password strength evaluation
# -------------------------
def evaluate_password_strength(password):
    length_criteria = len(password) >= 12
    digit_criteria = bool(re.search(r"\d", password))
    uppercase_criteria = bool(re.search(r"[A-Z]", password))
    lowercase_criteria = bool(re.search(r"[a-z]", password))
    symbol_criteria = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>\\[\\]\-_+=~`;'\\/\\\\]", password))

    score = sum([length_criteria, digit_criteria, uppercase_criteria, lowercase_criteria, symbol_criteria])

    if score == 5:
        return "Very Strong"
    elif score == 4:
        return "Strong"
    elif score == 3:
        return "Moderate"
    elif score == 2:
        return "Weak"
    else:
        return "Very Weak"

# -------------------------
#
