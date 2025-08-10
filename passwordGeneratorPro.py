import random
import string
import tkinter as tk
from tkinter import messagebox
import re

# --------------- Mnemonic Mappings ----------------
# These mappings help create memory-friendly hints for each password character

# NATO phonetic alphabet for uppercase letters
phonetic_map_upper = {
    letter: word for letter, word in zip(string.ascii_uppercase,
    ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel",
     "India", "Juliet", "Kilo", "Lima", "Mike", "November", "Oscar", "Papa",
     "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey",
     "X-ray", "Yankee", "Zulu"])
}

# Lowercase variant, derived from the uppercase map
phonetic_map_lower = {
    letter.lower(): phonetic_map_upper[letter].lower()
    for letter in phonetic_map_upper
}

# Mappings to read digits as words
digit_map = {
    "0": "Zero", "1": "One", "2": "Two", "3": "Three", "4": "Four",
    "5": "Five", "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine"
}

# Common symbol to descriptive name mapping
symbol_map = {
    "@": "At", "#": "Hash", "$": "Dollar", "%": "Percent", "&": "Ampersand",
    "*": "Star", "!": "Exclaim", "?": "Question", ".": "Dot", ",": "Comma",
    "+": "Plus", "-": "Dash", "_": "Underscore", "=": "Equals", "^": "Caret",
    "~": "Tilde", "/": "Slash", "\\": "Backslash", "(": "OpenParen", ")": "CloseParen"
}

# Name of the file where passwords will be saved
PASSWORD_STORE_FILE = "saved_passwords.txt"

# --------------- Password Generation ----------------
def generate_password(length, use_digits, use_uppercase, use_lowercase, use_symbols):
    """
    Generate a secure password based on user preferences.
    Guarantees that at least one of each selected character type is present.
    """
    char_types = []
    if use_digits:
        char_types.append(string.digits)
    if use_uppercase:
        char_types.append(string.ascii_uppercase)
    if use_lowercase:
        char_types.append(string.ascii_lowercase)
    if use_symbols:
        char_types.append(string.punctuation)

    # If user didn't select any type, raise an error
    if not char_types:
        raise ValueError("At least one character type must be selected")

    # Ensure at least one char from each selected set (stronger password)
    password = [random.choice(chars) for chars in char_types]

    # Fill remaining spots randomly from all selected types
    remaining_length = length - len(password)
    all_chars = ''.join(char_types)
    password += [random.choice(all_chars) for _ in range(remaining_length)]

    # Shuffle to avoid predictable placement
    random.shuffle(password)

    return ''.join(password)

# --------------- Mnemonic Hint Creation ----------------
def generate_hint(password):
    """
    Convert each character in the password into a human-readable word
    to build a memory-friendly hint that covers the entire password.
    """
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
            # Fallback for unsupported characters
            hint_parts.append(f"[{ch}]")  
    return " ".join(hint_parts)

# -------- Save password to file ----------
def save_password(password, filename=PASSWORD_STORE_FILE):
    """
    Append the generated password to a local file.
    """
    try:
        with open(filename, 'a') as f:
            f.write(password + '\n')
        return True  # Save successful
    except Exception as e:
        print(f"Error saving password: {e}")
        return False

# --------- Password strength evaluation -------------
def evaluate_password_strength(password):
    """
    Returns a strength rating from:
    'Very Weak', 'Weak', 'Moderate', 'Strong', or 'Very Strong'
    based on length and variety of character classes.
    """
    # Check presence of different character types
    length_criteria = len(password) >= 12
    digit_criteria = bool(re.search(r"\d", password))
    uppercase_criteria = bool(re.search(r"[A-Z]", password))
    lowercase_criteria = bool(re.search(r"[a-z]", password))
    symbol_criteria = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>\\[\\]\-_+=~`;'\\/\\\\]", password))

    score = sum([length_criteria, digit_criteria, uppercase_criteria, lowercase_criteria, symbol_criteria])

    # Return based on score
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

# --------------- GUI App ----------------
class PasswordGeneratorApp:
    """Graphical interface for password generation."""
    def __init__(self, root):
        print("Initializing GUI App...")  # Debug print
        self.root = root
        self.root.title("Password Generator")
        self.current_password = None  # Will store the last generated password
        self.setup_widgets()
        print("GUI widgets set up.")

    def setup_widgets(self):
        """Create and arrange all GUI elements."""
        tk.Label(self.root, text="Password Length:").grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=12)
        self.length_entry = tk.Entry(self.root, textvariable=self.length_var, width=10)
        self.length_entry.grid(row=0, column=1, sticky="w")

        # User preferences through checkboxes
        self.digits_var = tk.BooleanVar(value=True)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        tk.Checkbutton(self.root, text="Include Digits", variable=self.digits_var).grid(row=1, column=0, sticky="w")
        tk.Checkbutton(self.root, text="Include Uppercase", variable=self.uppercase_var).grid(row=1, column=1, sticky="w")
        tk.Checkbutton(self.root, text="Include Lowercase", variable=self.lowercase_var).grid(row=2, column=0, sticky="w")
        tk.Checkbutton(self.root, text="Include Symbols", variable=self.symbols_var).grid(row=2, column=1, sticky="w")

        # Generate Password button
        self.generate_button = tk.Button(self.root, text="Generate Password", command=self.generate_password_gui)
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Output box to display password and hint
        self.password_display = tk.Text(self.root, height=4, width=60, wrap=tk.WORD)
        self.password_display.grid(row=4, column=0, columnspan=2)

        # Save button (disabled initially)
        self.save_button = tk.Button(self.root, text="Save Password", command=self.save_password_gui, state=tk.DISABLED)
        self.save_button.grid(row=5, column=0, columnspan=2, pady=5)

        # Strength label
        self.strength_label = tk.Label(self.root, text="", font=("Arial", 10, "bold"))
        self.strength_label.grid(row=6, column=0, columnspan=2, pady=5)

    def generate_password_gui(self):
        """Triggered by 'Generate Password' button."""
        print("Generating password...")
        length = self.length_var.get()
        use_digits = self.digits_var.get()
        use_uppercase = self.uppercase_var.get()
        use_lowercase = self.lowercase_var.get()
        use_symbols = self.symbols_var.get()

        try:
            password = generate_password(length, use_digits, use_uppercase, use_lowercase, use_symbols)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        hint = generate_hint(password)
        strength = evaluate_password_strength(password)

        # Display results in text widget
        self.password_display.delete(1.0, tk.END)
        self.password_display.insert(tk.END, f"Password: {password}\nMemory Hint: {hint}\nStrength: {strength}")

        # Store password and enable save
        self.current_password = password
        self.save_button.config(state=tk.NORMAL)
        self.strength_label.config(text=f"Password Strength: {strength}")
        print("Password generated and displayed.")

    def save_password_gui(self):
        """Triggered by 'Save Password' button."""
        print("Saving password...")
        if self.current_password:
            if save_password(self.current_password):
                messagebox.showinfo("Success", f"Password saved to {PASSWORD_STORE_FILE}")
                self.save_button.config(state=tk.DISABLED)
                print("Password saved successfully.")
            else:
                messagebox.showerror("Error", "Failed to save password")
                print("Failed to save password.")

# --------------- Main ---------------
if __name__ == "__main__":
    print("Starting Password Generator GUI...")  # Debug print
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
    print("GUI closed.")  # Debug print
